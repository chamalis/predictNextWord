import unittest
from parser import *
from classifier import Classifier
from collections import defaultdict

class TestParser(unittest.TestCase):

    def setUp(self):
        #Sentence is : 3 times, This sentence: 2 times - case insensitive
        self.text = "Line1: Sentence is! This sentence isn't no3.\n" \
                    "Line2 starts here. This sentence is 4, ok?\r\n" \
                    "There are two bigrams repeating above"
        self.sentencesWithoutStemming =  \
                    [ "line1 sentence is", "this sentence isnt no3",
                      "line2 starts here", "this sentence is 4 ok",
                      "there are two bigrams repeating above"]
        self.num_bigrams   = 14      #the unique ones
        self.num_sentences = 5
        #Classifier class, encapsulates the 'update_bigrams' method, so:
        self.classifier = Classifier(verbose=True)  
    
    def test_split_sentences(self):
        
        sentences = split_sentences(self.text)
        self.assertEqual(type(sentences).__name__, 'list')
        self.assertEqual(len(sentences), self.num_sentences)

    def test_remove_stemming(self):
        
        sentences = split_sentences(self.text)
        sentencesWithoutStemming = remove_stemming (sentences)
        #print sentencesWithoutStemming
        self.assertItemsEqual (sentencesWithoutStemming, 
                               self.sentencesWithoutStemming)

    def test_make_bigrams(self):
        
        sentences = split_sentences(self.text)
        sentencesWithoutStemming = remove_stemming (sentences)
        allBigrams = defaultdict(int)
        for s in sentencesWithoutStemming:
            self.assertIsInstance(s, str)
            newBigrams = make_bigrams(s)
            #print '\n\n'
            #for k,v in newBigrams.items():
                #print k,v
            self.assertIsInstance(newBigrams, defaultdict)
            merge_and_sum_bigrams(allBigrams, newBigrams)

        self.classifier.update_joint_apriori(allBigrams)
        #for k,v in self.classifier.apriori.items():
            #print k,v
        self.assertEqual (len(allBigrams), self.num_bigrams)
    
    def assertDictEqual(self, d1, d2, msg=None): # assertEqual uses for dicts
        for k,v1 in d1.iteritems():
            self.assertIn(k, d2, msg)
            v2 = d2[k]
            if(isinstance(v1, collections.Iterable) and
               not isinstance(v1, basestring)):
                self.assertItemsEqual(v1, v2, msg)
            else:
                self.assertEqual(v1, v2, msg)
        return True
    
    def test_save_load(self):
        sentences = split_sentences(self.text)
        sentencesWithoutStemming = remove_stemming (sentences)
        allBigrams = defaultdict(int)
        for s in sentencesWithoutStemming:
            newBigrams = make_bigrams(s)
            merge_and_sum_bigrams(allBigrams, newBigrams)

        self.classifier.update_joint_apriori(allBigrams)
        
        for k,v in self.classifier.apriori.items():
            print k,v
        
        self.classifier.save('testC')
        newClassifier = Classifier()
        newClassifier.load('testC')
        #self.assertDictEqual(self.classifier.apriori, newClassifier.apriori)
        print '\nCOMPARE\n'
        for k,v in self.classifier.apriori.items():
            print k,v
        for k,v in newClassifier.apriori.items():
            print k,v
        print '\nEND OF COMPARE\n'
    '''
    def test_train(self):
        
        sentences = split_sentences(self.text)
        sentencesWithoutStemming = remove_stemming (sentences)
        allBigrams = defaultdict(int)
        for s in sentencesWithoutStemming:
            self.assertIsInstance(s, str)
            newBigrams = make_bigrams(s)
            self.assertIsInstance(newBigrams, defaultdict)
            merge_and_sum_bigrams(allBigrams, newBigrams)
        self.assertEqual (len(allBigrams), self.num_bigrams)
        
        #Here we test train:
        self.classifier.train()
        self.classifier.print_probs()
        print self.classifier.classify('Sentence')
    '''
    
if __name__ == '__main__':
    unittest.main()
