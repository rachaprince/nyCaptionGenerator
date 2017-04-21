import os
import shelve
import requests
import json
import itertools
import nltk
from nltk.parse import stanford
from nltk.internals import find_jars_within_path
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic
from nltk.wsd import lesk

HEADERS = {'Ocp-Apim-Subscription-Key': '2608430a171d4ed8ad3871d5067042f4'}
PAYLOAD = {'model': 'body', 'order': 1}
NEG_INFITE_LOG = -1000
brown_ic = wordnet_ic.ic('ic-brown.dat')

os.environ['STANFORD_PARSER'] = './jars'
os.environ['STANFORD_MODELS'] = './jars'
MODEL_PATH = './jars/englishPCFG.ser.gz'

def extract_words(stree):
    words = []
    stop = set(stopwords.words('english'))
    lmtzr = WordNetLemmatizer()
    st = LancasterStemmer()

    words += stree.leaves()
    words = [ item for item in words if item not in stop] # remove stopwords
    words =  [st.stem(item) if wordnet.synsets(st.stem(item)) else item.lower() for item in words] # stem if word
    words = [lmtzr.lemmatize(item) for item in words] # lemmatize
    return words

def score_words(words):
    scores = []

    with open('../apiCalls', 'r+') as apiFile:
        line = apiFile.readline()
        total_calls = int(line.split()[-1])

        lookupShelve = shelve.open('../lookup_shelve.db')

        for word in words:

            if str((word, 1, 'joint')) in lookupShelve:
                result = float(lookupShelve[str((word, 1, 'joint'))])
            else:
                body = { "queries": [ word ] }
                r = requests.post('https://westus.api.cognitive.microsoft.com/text/weblm/v1.0/calculateJointProbability', headers = HEADERS, params = PAYLOAD, data = json.dumps(body) )
                result = float(r.json()['results'][0]['probability'])

                lookupShelve.update({str((word, 1 , 'joint')): result})

                total_calls += 1

            scores.append((word, result))

        apiFile.seek(0)
        apiFile.write('total calls ' + str(total_calls))
        apiFile.close()

    return sorted(scores, key=lambda x: x[1], reverse = True)

def select_keyword(ranked_candidates, sent):
    pair = [None , None]
    pairs = []
    min_similarity = 1

    if not ranked_candidates:
        return (pair , pairs) # no possible keywords, no noun phrases

    # If only one NP, return 2 words with greatest log probability
    elif len(ranked_candidates) == 1:
        # print ranked_candidates
        # print ranked_candidates[-1]
        # print ranked_candidates[0]
        if len(ranked_candidates[0]) > 1:
            return ( [ranked_candidates[0][0][0], ranked_candidates[0][-1][0] ] , pair)
        else:
            return (pair, pair)

    # If 2+ sets of NP, return only pairs of words not from the same NP
    else:
        sent = nltk.word_tokenize(sent)

        results =  list(itertools.product(*ranked_candidates))
        for result in results:
            pairs.append(sorted(result, key= lambda x: x[1], reverse = True))

        # find highest ranking pair
        max_score = NEG_INFITE_LOG
        for result in pairs:
            score = result [0][1] # max score in the pairs
            if score > max_score:
                # find the right synset
                # w1 = lesk(sent, result[0][0])
                # w2 = lesk(sent, result[1][0])
                # similarity = w1.wup_similarity(w2)
                # # choose least similar words
                # if similarity < min_similarity:
                #     min_similarity = similarity
                max_score = score
                pair = [result[0][0] , result[-1][0]]


    return pair, pairs

def keyphrase_extract(sent):
    parser = stanford.StanfordParser(model_path=MODEL_PATH)
    parser._classpath = tuple(find_jars_within_path(os.environ['STANFORD_PARSER']))
    sentences = parser.raw_parse_sents([sent])

    candidates = []
    for line in sentences:
        for sentence in line:
            # print sentence
            for np_subtree in sentence.subtrees(filter=lambda x: x.label()== 'NP' or x.label() == 'VB'):
                words = extract_words(np_subtree)
                candidates.append(words)

    # in case of nested subtrees, remove subsets
    candidates_2 = candidates[:]

    for l in candidates:
        for l2 in candidates:
            if set(l).issubset(set(l2)) and l != l2:
                candidates_2.remove(l)
                break

    ranked_candidates = []
    # print candidates_2
    for word in candidates_2:
        ranked_candidates.append(score_words(word))

    # print ranked_candidates
    # exit()

    key_phrase_list = select_keyword(ranked_candidates, sent)
    return key_phrase_list


if __name__ == "__main__":
    # sent = "Helpful people are not being helpful; man covered in the dirt"
    # sent = 'Huge birds'
    sent = 'there is a desert island in a fish bowl with a small man'
    keyphrase_extract(sent)
