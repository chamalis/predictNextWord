#!/usr/bin/python

import cPickle, argparse

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_object', default=None,
        help='give file path to load trained object')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
        action="store_true")
    parser.add_argument("-w", "--word", required=True, 
        help="give word to classify")
    args = parser.parse_args()
    
    try:
        f = file(args.file_object, 'rb')
        classifier = cPickle.load(f)
        f.close()
        res = classifier.classify(args.word)
        print '\"'+args.word+'\"', 'is most probably followed by: "' \
               +res[0]+ '" with probability: ', res[1]
        
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]    

if __name__ == "__main__":
    main()
