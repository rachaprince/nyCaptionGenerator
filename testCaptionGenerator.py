import unittest
from phrasedictionary import PhraseDictionary
from captionGenerator import CaptionGenerator
import pickle

class TestCaptionGenerator(unittest.TestCase):

    # def test_init(self):
    #     #phrase_dict = PhraseDictionary(['phrases.txt'])
    #     with file('phrases.model', 'rb') as f:
    #         phrase_dict = pickle.load(f)
    #         phrase_dict.create_index()
    #     caption_gen = CaptionGenerator(phrase_dict)
    #     self.assertEqual(caption_gen.phrase_dict, phrase_dict)
    #
    # def test_get_phrase(self):
    #     #phrase_dict = PhraseDictionary(['phrases.txt'])
    #     with file('phrases.model', 'rb') as f:
    #          phrase_dict = pickle.load(f)
    #          phrase_dict.create_index()
    #     caption_gen = CaptionGenerator(phrase_dict)
    #     phrases = caption_gen.get_phrase('house')
    #     # self.assertEqual(10, len(phrases))
    #     # self.assertEqual(10, len(set(phrases))) # assert unique
    #
    # def test_create_caption(self):
    #     #phrase_dict = PhraseDictionary(['phrases.txt'])
    #     with file('phrases.model', 'rb') as f:
    #         phrase_dict = pickle.load(f)
    #         phrase_dict.create_index()
    #     caption_gen = CaptionGenerator(phrase_dict)
    #
    #     phrases = caption_gen.get_phrase('doctor')
    #     print phrases
    #     captions = caption_gen.create_caption(phrases, 'mouse')
    #     print captions
    #
    #     # Need to add assertion statements
    #
    # def test_display_caption(self):
    #     phrase_dict = PhraseDictionary(['../phraseScrapers/proverbs_0.txt', '../phraseScrapers/phrases.txt'],3,10)
    #     phrase_dict.create_index()
    #     caption_gen = CaptionGenerator(phrase_dict)
    #
    #     phrases = caption_gen.get_phrase('business')
    #     captions = caption_gen.create_caption(phrases, 'scuba')

        #caption_gen.display_caption(captions, './cartoon-images/25.jpg')

    def test_save(self):
        # saving the latest model for TestCaptionGenerator
        # phrase_dict = PhraseDictionary(['phraseScrapers/cliches.txt', 'phraseScrapers/phrases.txt', 'phraseScrapers/proverbs_0.txt', 'phraseScrapers/quotes.txt', 'phraseScrapers/truisms_1.txt', 'phraseScrapers/truisms.txt'],3,30)
        with file('phrases.model', 'rb') as f:
            phrase_dict = pickle.load(f)
        phrase_dict.create_index()
        caption_gen = CaptionGenerator(phrase_dict)
        caption_gen.save('./captionGenerator.model')

    # def test_load(self):
    #     with file('captionGenerator.model', 'rb') as f:
    #         caption_gen = pickle.load(f)
    #     phrases = caption_gen.get_phrase('business')
    #     print phrases
    #     captions = caption_gen.create_caption(phrases, 'subway')
    #     print captions



if __name__ == '__main__':
    unittest.main()
