import re, sys, collections, pickle

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
lexicon = {} # python built in dictionary for the lexicon
temp_dict = {} # this is just for checking for duplicate words in a doc
# list of lists(for each term) of tuples (doc, times) for inverted file
# initialized to size 128, doubles each time it needs to extend
inv_file = [[] for i in range(128)]
curr_doc = 0 # counter for the doc numbers instead of parsing for value
inv_index = 0
for line in readfile:
	# print(curr_doc)
	if '<P ID=' in line and '>' in line:
		# adding words from last doc to inverted file structure
		for term in temp_dict:
			if len(inv_file) <= lexicon[term][2]:
				extension = [[] for i in range(len(inv_file))]
				inv_file.extend(extension)
			inv_file[lexicon[term][2]].append([curr_doc, temp_dict[term]])
		curr_doc += 1 # increment counters on each doc
		temp_dict.clear()
	elif '</P>' not in line:
		# make all letters lowercase, then use regular expression to get words
		line_words = re.sub('[^a-z\ \-\']+', " ", line.lower()).split()
		for word in line_words:
			# filter out stopwords, additional filter for one and two letter words
			if word not in stopwords and len(word) > 2:
				if word in lexicon:
					lexicon[word][1] += 1 # increment word count in dictionary
				else:
					lexicon[word] = [0,1, inv_index] # add to dictionary
					inv_index += 1
				if word in temp_dict:
					temp_dict[word] += 1
				elif word not in temp_dict:
					temp_dict[word] = 1
					if word in lexicon:
						lexicon[word][0] += 1 # increment doc count
inv_file = [x for x in inv_file if x != []]

bytecount = 0;
alpha_lex = collections.OrderedDict(sorted(lexicon.items()))
lex_list = list(alpha_lex.items()) # transfer dict to list for easier manipulation
collection_size = 0 	# counter for total number of words
# find total number of words
for k, v in lex_list:
	collection_size += v[1] # increment by word count

writefile.write('Number of Documents:' + str(curr_doc) + '\n')
writefile.write('Vocabulary size:' + str(len(lexicon)) + '\n')
writefile.write('Total number of words:' + str(collection_size) + '\n')

# write inverted list to binary file
with open('inv_' + fname[:-4] + '.bin', 'wb') as invertedfile:
	for word in alpha_lex:
		postings_list = inv_file[alpha_lex[word][2]]
		alpha_lex[word][2] = bytecount
		# print(postings_list)
		for post in postings_list:
			invertedfile.write(post[0].to_bytes(2, byteorder='big', signed=False))
			invertedfile.write(post[1].to_bytes(2, byteorder='big', signed=False))
			bytecount += 2

# write lexicon to pickled file
pickle.dump(alpha_lex, open(fname[:-4] + '.pkl', 'wb'))


