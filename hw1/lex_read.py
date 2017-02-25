import pickle, sys

# function for retrieving postings list
def get_list(lexicon, inv_file, word):
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
def get_df(lexicon, word):
	if word.lower() in lexicon:
		return lexicon[word][0]
	else:
		return -1

fname = sys.argv[1]
# open the two saved files
new_alphalex = pickle.load(open(fname, 'rb'))
f = open('postings_' + fname[:-4] + '.txt', 'w')

# read in the inverted file
inv_list = []
with open('inv_' + fname[:-4] + '.bin', 'rb') as invertedfile:
	while True:
		intbytes = invertedfile.read(2)
		if not intbytes:
			break
		inv_list.append(int.from_bytes(intbytes, byteorder='big', signed=False))

# print out the information needed
f.write('archer postings list: ' + get_list(new_alphalex, inv_list, 'archer') + '\n')
f.write('blameless postings list: ' + get_list(new_alphalex, inv_list, 'blameless') + '\n')
f.write('study postings list: ' + get_list(new_alphalex, inv_list, 'study') + '\n')
f.write('nuclear postings list: ' + get_list(new_alphalex, inv_list, 'nuclear') + '\n')
f.write('horse document frequency: ' + str(get_df(new_alphalex, 'horse')) + '\n')
f.write('lovingkindness document frequency: ' + str(get_df(new_alphalex, 'lovingkindness')) + '\n')
f.write('mary document frequency: ' + str(get_df(new_alphalex, 'mary')) + '\n')
f.write('dance document frequency: ' + str(get_df(new_alphalex, 'dance')) + '\n')

