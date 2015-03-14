import re
from collections import defaultdict, Counter   #defaultdict needs python > 2.5  
from itertools import izip, islice

def split_sentences(text):
    ''' Break a text into sentences and return a list.'''

    sentenceEnders = re.compile('[.!?]')
    sentenceList = sentenceEnders.split(text)
    sentenceList = [s.strip() for s in sentenceList]
    return sentenceList

def remove_stemming(sentenceList):
    '''Cleans each sentence from punctuation '''
    
    cleanSentences = []
    for s in sentenceList:
        assert type(s).__name__ == 'str'
        tmp = re.sub('[\[!#$%&()*+,-.:;<=>?@^_{|}~\'\"\]]', '', s)
        clean = tmp.replace("\r\n"," ")
        clean = clean.replace("\\", "")
        clean = clean.lower()
        cleanSentences.append(clean)
    return cleanSentences

def make_bigrams(s):
    '''Builds bigrams as defaultdicts where key is the a tuple containing two strings
       (each word), and the value is its frequency. E.g ('I', 'am'): 2. For example
       a complete bigram: defaultdict(<type 'int'>, 
       {('aqs', 'hello'): 1, ('what', 'hello'): 1, ('hello', 'man'): 2, ('man', 'what'): 1})
       Each bigram must be fed to Classifier.update_joint_apriori(bigram)
    '''
    words = s.split(' ')
    d = defaultdict(int, Counter(izip(words, islice(words, 1, None))))
    return d
    
def merge_and_sum_bigrams(bigrams1, bigrams2):
    
    for k,v in bigrams2.items():
        #bigram is defaultdict so even if k not a key it will be added
        bigrams1[k] += bigrams2[k]     
