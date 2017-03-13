import re, sys, collections, pickle, math

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
writefile = open('analysis_' + fname, 'w')
# python built in dictionary for the lexicon
# word:[doc_freq, term_freq, index, tdidf]
lexicon = {}
temp_dict = {} # this is just for checking for duplicate words in a doc
# list of lists(for each term) of tuples (doc, times) for inverted file
# initialized to size 128, doubles each time it needs to extend
inv_file = [[] for i in range(128)]
curr_doc = 0 # counter for the doc numbers instead of parsing for value
total_docs = 0
inv_index = 0

for line in readfile:
	# print(curr_doc)
	if '<P ID=' in line and '>' in line:
		curr_doc = int(re.search(r'\d+', line).group()) # increment counters on each doc
		total_docs += 1
		if curr_doc % 1000 == 0:
			print(curr_doc)
	elif '</P>' in line:
		# adding words from last doc to inverted file structure
		for term in temp_dict:
			if len(inv_file) <= lexicon[term][2]:
				extension = [[] for i in range(len(inv_file))]
				inv_file.extend(extension)
			inv_file[lexicon[term][2]].append([curr_doc, temp_dict[term]])
		temp_dict.clear()
	elif '</P>' not in line:
		# make all letters lowercase, then use regular expression to get words
		line_words = re.sub('[^a-z\ \-\']+', " ", line.lower()).split()
		for word in line_words:
			# filter out stopwords, additional filter for one and two letter words
			if word not in stopwords and len(word) > 2:
				if word[:5] in lexicon:
					lexicon[word[:5]][1] += 1 # increment word[:5] count in dictionary
				else:
					lexicon[word[:5]] = [0,1, inv_index, 0] # add to dictionary
					inv_index += 1
				if word[:5] in temp_dict:
					temp_dict[word[:5]] += 1
				elif word[:5] not in temp_dict:
					temp_dict[word[:5]] = 1
					if word[:5] in lexicon:
						lexicon[word[:5]][0] += 1 # increment doc count
inv_file = [x for x in inv_file if x != []]
bytecount = 0;
alpha_lex = collections.OrderedDict(sorted(lexicon.items()))
lex_list = list(alpha_lex.items()) # transfer dict to list for easier manipulation
collection_size = 0 	# counter for total number of words
# find total number of words
for k, v in lex_list:
	collection_size += v[1] # increment by word count

writefile.write('Number of Documents:' + str(total_docs) + '\n')
writefile.write('Vocabulary size:' + str(len(lexicon)) + '\n')
writefile.write('Total number of words:' + str(collection_size) + '\n')

# write inverted list to binary file
with open('inv_' + fname[:-4] + '_stem.bin', 'wb') as invertedfile:
	for word in alpha_lex:
		postings_list = inv_file[alpha_lex[word][2]]
		alpha_lex[word][2] = bytecount
		alpha_lex[word][3] = math.log(total_docs/alpha_lex[word][0], 2) #compute td/idf
		if word == 'archer':
			print(alpha_lex[word][3])
		# print(postings_list)
		for post in postings_list:
			invertedfile.write(post[0].to_bytes(4, byteorder='big', signed=False))
			invertedfile.write(post[1].to_bytes(4, byteorder='big', signed=False))
			bytecount += 2
		if 'dace' in word:
			print(word)

# calculate document lengths
doc_lens = {}
curr_doc = -1
readfile.seek(0)
for line in readfile:
	if '<P ID=' in line and '>' in line:
		curr_doc = int(re.search(r'\d+', line).group()) # increment counters on each doc
		if curr_doc % 1000 == 0:
			print(curr_doc)

	elif '</P>' in line:
		# adding words from last doc to inverted file structure
		len_accum = 0
		for word, count in temp_dict.items():
			len_accum += alpha_lex[word][3] * alpha_lex[word][3] * count * count
		doc_lens[curr_doc] = math.sqrt(len_accum)
		# print(doc_lens[curr_doc])
		temp_dict.clear()
	elif '</P>' not in line:
		# make all letters lowercase, then use regular expression to get words
		line_words = re.sub('[^a-z\ \-\']+', " ", line.lower()).split()
		for word in line_words:
			# filter out stopwords, additional filter for one and two letter words
			if word not in stopwords and len(word) > 2:
				if word[:5] not in temp_dict:
					temp_dict[word[:5]] = 1
				else:
					temp_dict[word[:5]] += 1
				# print(word, alpha_lex[word][3])
				# len_accum += alpha_lex[word][3] * alpha_lex[word][3] * * 
				
# write lexicon to pickled file
pickle.dump(alpha_lex, open(fname[:-4] + '_stem.pkl', 'wb'))
pickle.dump(doc_lens, open(fname[:-4] + '_lengths_stem.pkl', 'wb'))
with open(fname[:-4] + 'size.txt', 'w') as sizefile:
	sizefile.write(str(total_docs))



