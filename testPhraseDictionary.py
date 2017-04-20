import unittest
from phrasedictionary import PhraseDictionary
import os

TEXT_FILES_PATH = '../phraseScrapers/'
MIN_WORDS = 5
MAX_WORDS = 20

class TestPhraseDictionary(unittest.TestCase):

    # def test_init(self):
    #     filename = 'temp.txt'
    #     # create a file
    #     outFile = open(filename, 'w')
    #     outFile.write('This is test sentence one\nThis is test sentence two\n')
    #     outFile.close()
    #
    #     # load word2vecModel
    #     #model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)
    #
    #     phrase_dict = PhraseDictionary([filename],3,20)
    #
    #     # assert dicitonary right format
    #     result = len(phrase_dict.phrases)
    #     self.assertEqual(2, result)
    #     result = len(list(phrase_dict.phrases)[0].split(' '))
    #     self.assertEqual(5, result)
    #     self.assertFalse('\n' in list(phrase_dict.phrases)[1].split(' '))
    #
    #     #self.assertTrue(phrase_dict.model is model)

    # def test_create_index(self):
    #     filename = 'temp.txt'
    #     # create a file
    #     outFile = open(filename, 'w')
    #     outFile.write('This is test sentence one\nThis is test sentence two\n')
    #     outFile.close()
    #
    #     # load word2vecModel
    #     #model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)
    #
    #     phrase_dict = PhraseDictionary([filename],3,20)
    #     phrase_dict.create_index()
    #
    #     # Need to add tests
    #
    # def test_search(self):
    #     filename = 'temp.txt'
    #     # create a file
    #     outFile = open(filename, 'w')
    #     outFile.write('This is test sentence one\nThis is test sentence two\n')
        # outFile.close()
        #
        # phrase_dict = PhraseDictionary([filename],3,20)
        # phrase_dict.create_index()
        #
        # results = phrase_dict.search("one")
        # print results
        #
        # phrase_dict_1 = PhraseDictionary(['../phraseScrapers/phrases.txt'],5,100)
        # phrase_dict_1.create_index()
        #
        # results = phrase_dict_1.search('doctor')
        # print results

        # gonna need gensims for this

    def test_save(self):
        # saving the latest model for TestCaptionGenerator
        # phrase_dict = PhraseDictionary(['../phraseScrapers/cliches.txt', '../phraseScrapers/phrases.txt', '../phraseScrapers/proverbs_0.txt', '../phraseScrapers/quotes.txt', '../phraseScrapers/truisms_1.txt', '../phraseScrapers/truisms.txt'],5,25)
        files = [ os.path.join(TEXT_FILES_PATH, i) for i in os.listdir(TEXT_FILES_PATH) if os.path.isfile(os.path.join(TEXT_FILES_PATH,i)) and i.startswith('preprocessed')]
        phrase_dict = PhraseDictionary(files, MIN_WORDS, MAX_WORDS)
        phrase_dict.create_index()
        phrase_dict.save('./phrases.model')
        print len(phrase_dict.phrases)
        # results = phrase_dict.search('apple')
        # print results




if __name__ == '__main__':
    unittest.main()
