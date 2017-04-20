from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh import searching
import pickle
import gensim
import requests
import json
import shelve

# files == list of .txt files, each line a phrase, separated by a new line
# min == min length of sentence
# max == max length of sentence
# model == word2vec model location
class PhraseDictionary(object):
    def __init__(self, filenames, min_len, max_len):
        # load the files into phrases
        self.phrases = set()
        for filename in filenames:
            with open(filename) as f:
                for line in f.read().splitlines():
                    words = line.split(' ')
                    if len(words) > min_len and len(words) < max_len:
                        self.phrases.add(line)

        # self.model = gensim.models.KeyedVectors.load_word2vec_format(model, binary = True)
        self.ix = None
        self.headers = {'Ocp-Apim-Subscription-Key': '2608430a171d4ed8ad3871d5067042f4'}
        self.payload = {'model': 'body', 'order': 1}

        # self.vector_dict = {}
        # self.phrases_vectors = []

    # scoring function for ranked retrieval of the documents
    def ngram_score_fn(self, searcher, fieldname, text, matcher):
        result = None

        with open('../apiCalls', 'r+') as apiFile:
            line = apiFile.readline()
            total_calls = int(line.split()[-1])

            phrase = self.ix.searcher().stored_fields(matcher.id())['content']

            scores = []
            # body = { "queries": [ phrase ] }

            lookupShelve = shelve.open('lookup_shelve.db')

            if str((phrase, 1, 'joint')) in lookupShelve:
                result = lookupShelve[str((phrase, 1, 'joint'))]
            else:
                body = { "queries": [ phrase ] }
                r = requests.post('https://westus.api.cognitive.microsoft.com/text/weblm/v1.0/calculateJointProbability', headers = self.headers, params = self.payload, data = json.dumps(body) )
                result = r.json()['results'][0]['probability']

                lookupShelve.update({str((phrase, 1 , 'joint')): result})

                total_calls += 1

            apiFile.seek(0)
            apiFile.write('total calls ' + str(total_calls))
            apiFile.close()

        return result

    # call this on the init?
    def create_index(self):
        self.schema = Schema(index = ID(stored = True), content = TEXT(stored = True))
        self.ix = create_in("indexdir", self.schema)
        writer = self.ix.writer()
        for i, p in enumerate(self.phrases):
            writer.add_document(index = str(i).decode('utf-8'), content = p.decode('utf-8'))
        writer.commit()
        return

    def search(self, keyword):
        # similar_words = self.model.similar_by_word(keyword, topn=10, restrict_vocab=None)
        # similar_words.insert(0,keyword)
        # for word in similar_words:
        ngram_weighting = scoring.FunctionWeighting(self.ngram_score_fn)
        with self.ix.searcher(weighting=ngram_weighting) as searcher:
            query = QueryParser("content", schema=self.ix.schema).parse(keyword)
            result_indexes = searcher.search(query, limit=10)
            results = [ r['content'] for r in result_indexes ]
        return results

    def save(self, f):
        f = file(f, 'wb')
        pickle.dump(self, f)
        f.close()

    def del_model(self):
        del self.model
