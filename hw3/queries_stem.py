import re, sys, collections, pickle, math, operator

# function for finding all documents that match a query
def get_docs(lexicon, inv_file, words):
	docs = []
	for word in words:
		word_docs = get_postings_list(lexicon, inv_file, word)
		for doc, count in word_docs:
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
			retval.append([doc, count])
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
		return lexicon[word][3]
	else:
		print('tdidf not found', word)
		return -1

def build_search_matrix(lexicon, inv_file, words):
	docs = get_docs(lexicon, inv_file, words)
	#declare empty matrix
	matrix = {}
	#fill matrix with zeroes
	for doc in docs:
		matrix[doc] = {}
		for word in words:
			matrix[doc][word] = 0
	#fill in nonzero values of matrix
	for word in words:
		posts = get_postings_list(lexicon, inv_file, word)
		for doc, count in posts:
			if doc in matrix:
				matrix[doc][word] = count * get_tdidf(lexicon, word)
	return matrix

# takes "length" of document, document vector(dict), with only query terms, query vector
def cosine(doc_len, doc_vec, q_vec):
	# check for matching lengths
	if len(doc_vec) != len(q_vec):
		return -1
	# get "length" of query vector
	q_len = 0
	for value in q_vec.values():
		q_len += value * value
	q_len = math.sqrt(q_len)
	num = 0
	for word in q_vec.keys():
		num += q_vec[word] * doc_vec[word]
	if num != 0:
		if num / (q_len * doc_len) > 1:
			print('cosine greater than 1', num, doc_len, q_len, doc_vec, q_vec)
		return num / (q_len * doc_len)
	else:
		return 0

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
query_file = sys.argv[1]
inv_file = sys.argv[2]
pkl_file = sys.argv[3]
readfile = open(query_file, 'r')
#read in lexicon pickle file
new_alphalex = pickle.load(open(pkl_file, 'rb'))
# representation of queries
# dictionary of list of pairs with (term, count)
qs = {}

curr_q = -1 # query number
total_q = 0
inv_index = 0
# one for each query
# format: {word:count, word:count}
term_pairs = {}
for line in readfile:
	if '<Q ID=' in line and '>' in line:
		curr_q = int(re.search(r'\d+', line).group()) # find query number
		total_q += 1

	elif '</Q>' in line:
		qs[curr_q] = term_pairs.copy()
		term_pairs.clear()
	elif '</Q>' not in line:
		# make all letters lowercase, then use regular expression to get words
		line_words = re.sub('[^a-z\ \-\']+', " ", line.lower()).split()

		for word in line_words:
			# filter out stopwords, additional filter for one and two letter words
			if word not in stopwords and len(word) > 2:
				if word in term_pairs:
					# increment word[:5] count in dictionary
					term_pairs[word[:5]] += get_tdidf(new_alphalex, word[:5])
				else:
					# add to dictionary
					term_pairs[word[:5]] = get_tdidf(new_alphalex, word[:5])


# read in the inverted file
inv_list = []
with open(inv_file, 'rb') as invertedfile:
	while True:
		intbytes = invertedfile.read(4)
		if not intbytes:
			break
		inv_list.append(int.from_bytes(intbytes, byteorder='big', signed=False))

doc_lens = pickle.load(open(pkl_file[:-8] + 'lengths_stem.pkl', 'rb'))
print('doc_lens', doc_lens)

# for each query, construct a matrix with terms in query as one axis
# and all documents containing query words as the other
# numeric value is times a term appears in a document
query_vectors = []
doc_matrices = []
rankings = {}
for query_num, query_vector in qs.items():
	print('loop', query_num)
	matrix = build_search_matrix(new_alphalex, inv_list, query_vector.keys())
	cosines = {}
	for doc_num, doc_vector in matrix.items():
		doc_length = doc_lens[doc_num]
		cosines[doc_num] = cosine(doc_length, doc_vector, query_vector)
	sorted_cosines = sorted(cosines.items(), key=operator.itemgetter(1))
	sorted_cosines.reverse()
	rankings[query_num] = sorted_cosines
	doc_matrices.append(matrix) #list of matrices
	query_vectors.append((query_num, query_vector)) #converting to a list

with open(query_file[:-4] + '_results-stem.txt', 'w') as w1:
	for q_num, rank in rankings.items():
		for index, entry in enumerate(rank):
			if index < 50:
				w1.write(str(q_num) + ' Q0 ' + str(entry[0]) +
					' ' + str(index + 1) + ' ' + str(entry[1]) + ' he\n')