import re
from collections import defaultdict   #needs python > 2.5
#from mongodict import MongoDict
#from pymongo import Connection

class Classifier:

    def __init__(self, verbose=False):
        ''' Apriori and joint are calculated each time a file is read.
            posterior is only calculated when a certain word is being evaluated
            Thus posterior['hello'] is the most probable word following 'hello'
            along with the corresponding probability '''
            
        self.apriori  = defaultdict(int)
        self.joint = defaultdict(int)
        #self.apriori = MongoDict(host='localhost', port=27017, database='next_word',
        #                    collection='apriori')
        #self.joint = MongoDict(host='localhost', port=27017, database='next_word',
        #                    collection='joint')
        self.posterior = defaultdict()
        self.verbose = verbose
        #self.connection = Connection()
        
    def update_joint_apriori(self, dict_bigrams):
        '''Every time an new file is read, the bigrams (defaultdicts) are created
           and the apriori && joint probs are updated '''
           
        for k, v in dict_bigrams.items():
            if type(k).__name__ != 'tuple' or len(k) != 2 or type(v).__name__!='int':   
                #sth is wrong
                if self.verbose:
                    print 'wrong bigram type, skipping:\t', k,v
                continue
            self.joint[k] += v
            self.apriori[k[0]] += v
        
        return self.joint  #redundant: just for unit testing
        
    def calculate_posterior(self, word):
        ''' For each word update the posterior (next word prediction).
            We want to maximize joint_prob(word,next) / prior(word)'''
        
        max = -1
        for k, v in self.joint.items():
            try:
                prev, next = k[0], k[1]
                assert type(prev).__name__ == 'str'
                assert type(next).__name__ == 'str'
                if prev == word:
                    postProb = round((v+1.0)/(self.apriori[word]+1.0), 2)
                    assert postProb <= 1.0
                    if postProb > max:
                        self.posterior[word] = (next, postProb)
                        max = postProb
            except ValueError:
                print 'got key: ', k , '\tvalue: ', v
    
    def pre_train(self):
        ''' To calculate all of the posteriors before the classifier (classify.py is runned).
            Computationally FORBIDABLE '''
        
        for k, v in self.apriori.items():
            self.calculate_posterior(k)
    
    def classify(self, word):
        '''clean the word and find the most probable follower (calculate_posterior)'''
        
        word = re.sub('[,!#$%&()*+,-.:;<=>?@^_{|}~]', '', word)
        word = word.lower()
        #searches for the most probable outcome based on joint and prior probs
        self.calculate_posterior(word)
        return self.posterior[word]
    
    def save(self, dbName):
        db = self.connection[dbName]
        db.apriori.insert(self.apriori)
        db.joint.insert(self.joint)
    
    def load(self, dbName):
        db = self.connection[dbName]
        self.apriori = db.apriori.find()  #its only one
        self.joint = db.joint.find()
    
    def print_probs(self):
        
        print 'apriori length (number of words): ', len(self.apriori)
        print 'joint length (number of bigrams): ', len(self.joint)
        
