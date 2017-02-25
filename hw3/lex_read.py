import pickle, sys

# function for retrieving postings list
def get_postings_list(lexicon, inv_file, word):
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

# function for retrieving document frequency
def get_doc_freq(lexicon, word):
	if word.lower() in lexicon:
		return new_alphalex[word][0]
	else:
		return -1

fname = sys.argv[1]
# open the two saved files
new_alphalex = pickle.load(open(fname, 'rb'))
writefile = open('postings_' + fname[:-4] + '.txt', 'w')
collection_size = 0
with open(fname[:-4] + 'size.txt', 'r') as sizefile:
	for line in sizefile:
		for num in line.split():
			collection_size = int(num)

# read in the inverted file
inv_list = []
with open('inv_' + fname[:-4] + '.bin', 'rb') as invertedfile:
	while True:
		intbytes = invertedfile.read(4)
		if not intbytes:
			break
		inv_list.append(int.from_bytes(intbytes, byteorder='big', signed=False))

# print out the information needed
writefile.write('archer postings list: ' +
	get_postings_list(new_alphalex, inv_list, 'archer') + '\n')
writefile.write('blameless postings list: ' +
	get_postings_list(new_alphalex, inv_list, 'blameless') + '\n')
writefile.write('study postings list: ' +
	get_postings_list(new_alphalex, inv_list, 'study') + '\n')
writefile.write('nuclear postings list: ' +
	get_postings_list(new_alphalex, inv_list, 'nuclear') + '\n')
writefile.write('horse document frequency: ' +
	str(get_doc_freq(new_alphalex, 'horse')) + '\n')
writefile.write('lovingkindness document frequency: ' +
	str(get_doc_freq(new_alphalex, 'lovingkindness')) + '\n')
writefile.write('mary document frequency: ' +
	str(get_doc_freq(new_alphalex, 'mary')) + '\n')
writefile.write('dance document frequency: ' +
	str(get_doc_freq(new_alphalex, 'dance')) + '\n')

