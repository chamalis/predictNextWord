Next word prediction: Take as input a word and return the most probable one to follow as well as the corresponding probability.
Maximum Likelihood is used on the bigrams extracted from the gutenberg books.

== DOWNLOAD DATASET ==

	$ sh download_guten.sh
	$ sh unzip.sh

you can execute the unzip.sh at any time (and many times),
without waiting for download_guten.sh to finish

== USAGE ==

Run example:

*** TRAINING: ***

	$ python src/train.py -d www.gutenberg.lib.md.us/ -fo trained.pickle -v

You can also retrain an instance (word frequencing will be summed, thus
if you run on the same dataset, documents will be double-evalueated):

	$ python src/train.py -d www.gutenberg.lib.md.us/ -fi trained_in.pickle -fo trained_out.pickle -v

*** CLASSIFY a random word:  ***

	$ python src/classify.py -f trained.pickle -w no

example output:

	$ python classify.py -w no -f trained_stopped.pickle

	$  "no" is most probably followed by: "one" with probability:  0.06

You can download the trained classifier (mentioned in REPORT) by:

	$ wget -c http://cineserver.3p.tuc.gr/nextWordPred/trained.pickle

== NOTICE ==

1) The train.py can consume all your RAM and virtual MEM space and may crash your OS.
2) SIGKILL (CTRL-C) signal handler will save the classifier (during train.py execution) at any point.

Assumptions:

1) Input is classified after removing special chars, for example:
   Input: "Title"     or
   Input: "title:"    
   are considered the same input.

2) If classifier is runned without been trained before it may produce
keyerrors etc..

