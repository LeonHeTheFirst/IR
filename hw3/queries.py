import re, sys, collections, pickle

# function for finding all documents that match a query
def get_docs(lexicon, inv_file, words):
	docs = []
	for word in words:
		word_docs = get_postings_list(lexicon, inv_file, word)
		for doc in word_docs:
			if doc not in docs:
				docs.append(doc)
	docs.sort()
	return docs

# function for retrieving postings list as a string
def get_postings_str(lexicon, inv_file, word):
	if word.lower() in lexicon:
		retval = ''
		# iterate through the values two at a time
		it = zip(*[iter(inv_file[lexicon[word][2]:lexicon[word][2]
			 + 2*lexicon[word][0]])]*2)
		for doc, count in it:
			retval += ' doc' + str(doc) + ': ' + str(count) + ','
		return retval[:-1] # remove last comma
	else:
		return 'not in lexicon'

# function for retrieving postings list
def get_postings_list(lexicon, inv_file, word):
	if word.lower() in lexicon:
		retval = []
		# iterate through the values two at a time
		it = zip(*[iter(inv_file[lexicon[word][2]:lexicon[word][2]
			 + 2*lexicon[word][0]])]*2)
		for doc, count in it:
			retval.append(doc)
		return retval
	else:
		return []

# function for retrieving document frequency
def get_doc_freq(lexicon, word):
	if word.lower() in lexicon:
		return lexicon[word][0]
	else:
		return -1
# function for retrieving td/idf
def get_tdidf(lexicon, word):
	if word.lower() in lexicon:
		return lexicon[word][0]
	else:
		return -1

def build_doc_vector():
	return

def cosine(doc_vec, q_vec):
	return

#list of stopwords taken from http://www.ranks.nl/stopwords
stopwords = ['a','about','above','after','again','against','all','am','an','and',
		'any','are','aren\'t','as','at','be','because','been','before','being',
		'below','between','both','but','by','can\'t','cannot','could','couldn\'t',
		'did','didn\'t','do','does','doesn\'t','doing','don\'t','down','during',
		'each','few','for','from','further','had','hadn\'t','has','hasn\'t','have',
		'haven\'t','having','he','he\'d','he\'ll','he\'s','her','here','here\'s',
		'hers','herself','him','himself','his','how','how\'s','i','i\'d','i\'ll',
		'i\'m','i\'ve','if','in','into','is','isn\'t','it','it\'s','its','itself',
		'let\'s','me','more','most','mustn\'t','my','myself','no','nor','not','of',
		'off','on','once','only','or','other','ought','our','ours','ourselves','out',
		'over','own','same','shan\'t','she','she\'d','she\'ll','she\'s','should',
		'shouldn\'t','so','some','such','than','that','that\'s','the','their','theirs',
		'them','themselves','then','there','there\'s','these','they','they\'d','they\'ll',
		'they\'re','they\'ve','this','those','through','to','too','under','until','up',
		'very','was','wasn\'t','we','we\'d','we\'ll','we\'re','we\'ve','were','weren\'t',
		'what','what\'s','when','when\'s','where','where\'s','which','while','who',
		'who\'s','whom','why','why\'s','with','won\'t','would','wouldn\'t','you',
		'you\'d','you\'ll','you\'re','you\'ve','your','yours','yourself','yourselves']
# open up the files to read and write, binary for the inverted file
fname = sys.argv[1]
readfile = open(fname, 'r')
# representation of queries
# dictionary of list of pairs with (term, count)
qs = {}

curr_q = -1 # query number
total_q = 0
inv_index = 0
term_pairs = {}
for line in readfile:
	if '<Q ID=' in line and '>' in line:
		if curr_q != -1:
			qs[curr_q] = term_pairs.items()
			term_pairs.clear()
		curr_q = int(re.search(r'\d+', line).group()) # increment counters on each doc
		total_q += 1

	elif '</Q>' not in line:
		# make all letters lowercase, then use regular expression to get words
		line_words = re.sub('[^a-z\ \-\']+', " ", line.lower()).split()

		for word in line_words:
			# filter out stopwords, additional filter for one and two letter words
			if word not in stopwords and len(word) > 2:
				if word in term_pairs:
					term_pairs[word] += 1 # increment word count in dictionary
				else:
					term_pairs[word] = 1 # add to dictionary
		
# print(qs[76]) #print out representation for first query

# read in the inverted file
inv_list = []
with open('inv_' + fname[:-4] + '.bin', 'rb') as invertedfile:
	while True:
		intbytes = invertedfile.read(4)
		if not intbytes:
			break
		inv_list.append(int.from_bytes(intbytes, byteorder='big', signed=False))
#read in lexicon pickle file
new_alphalex = pickle.load(open(fname[:-4] + '.pkl', 'rb'))

print(get_docs(new_alphalex, inv_list, ['archer', 'nuclear', 'blameless']))