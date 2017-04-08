import os, csv, pickle, re
from datetime import datetime
from operator import itemgetter
# function to read in the query data
def read_tsv(path):
	q_array = []
	with open(path) as tsv_file:
		date = '12-20-1999T'
		tsv = csv.reader(tsv_file, delimiter='\t')
		for line in tsv:
			# make datetime object
			# timestring = line[0][0:1] + ':' + line[0][2:3] + ':' + line[0][4:5]
			time = datetime.strptime(date + line[0], '%m-%d-%YT%H%M%S')
			q_array.append({'stamp': time, 'id': line[1], 'rank': int(line[2]), 'query': line[3]})
	return q_array

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

# read in the data from pickle file if you've already read it in before
if(os.path.isfile('queries.pkl')):
	q_array = pickle.load(open('queries.pkl', 'rb'))
else:
	q_array = read_tsv('19991220-Excite-QueryLog.utf8.tsv')
	pickle.dump(q_array, open('queries.pkl', 'wb'))

# Question 1
print()
print('Question 1')
unique_ids = {}
for q in q_array:
	if q['id'] not in unique_ids:
		unique_ids[q['id']] = 1
q_per_id = len(q_array) / len(unique_ids)
print('Total Length:', len(q_array))
print('Unique IDs:', len(unique_ids))
print('Queries per ID:', q_per_id)

# Question 2
print()
print('Question 2')
word_count = 0
char_count = 0
word_array = []
char_array = []
for q in q_array:
	char_count += len(q['query'])
	word_count += len(q['query'].split())
	char_array.append(len(q['query']))
	word_array.append(len(q['query'].split()))
print('Total characters:', char_count, 'mean:', char_count/len(q_array), 'median:', sorted(char_array)[int(len(char_array)/2)])
print('Total words:', word_count, 'mean:', word_count/len(q_array), 'median:', sorted(word_array)[int(len(word_array)/2)])

# Question 3
print()
print('Question 3')
mixed_count = 0
lower_count = 0
upper_count = 0
non_alpha_count = 0
for q in q_array:
	if not re.search('[a-zA-Z]', q['query']):
		non_alpha_count += 1
	elif q['query'].islower():
		lower_count += 1
	elif q['query'].isupper():
		upper_count += 1
	else:
		mixed_count += 1
print('Mixed Case:', mixed_count, 'percent:', mixed_count/len(q_array))
print('All Lowercase:', lower_count, 'percent:', lower_count/len(q_array))
print('All Uppercase:', upper_count, 'percent:', upper_count/len(q_array))
print('Non-Alphanumeric:', non_alpha_count, 'percent:', non_alpha_count/len(q_array))

# Question 4
print()
print('Question 4')
top_ten = 0
for q in q_array:
	if q['rank'] == 0:
		top_ten += 1
print('Using top ten:', top_ten, 'percent:', top_ten/len(q_array))

# Question 5
print()
print('Question 5')
question_count = 0
for q in q_array:
	if q['query'][:2].lower() == 'wh' or q['query'][-1:] == '?':
		question_count += 1
print('Question count:', question_count, 'percent:', question_count/len(q_array))

# Question 6
print()
print('Question 6')
query_bins = {}
for q in q_array:
	if q['query'].lower() in query_bins:
		query_bins[q['query'].lower()] += 1
	else:
		query_bins[q['query'].lower()] = 1
ranks = sorted(query_bins.items(), key=itemgetter(1), reverse=True)
for item in ranks[:20]:
	print(item)

# Question 7
print()
print('Question 7')
word_bins = {}
for q in q_array:
	for word in q['query'].lower().split():
		if word not in stopwords and re.search('[a-z]', word):
			if word in word_bins:
				word_bins[word] += 1
			else:
				word_bins[word] = 1
ranks = sorted(word_bins.items(), key=itemgetter(1), reverse=True)
for item in ranks[:20]:
	print(item)

# Question 8
print()
print('Question 8')
stopword_bins = {}
for q in q_array:
	for word in q['query'].lower().split():
		if word in stopwords:
			if word in stopword_bins and re.search('[a-z]', word):
				stopword_bins[word] += 1
			else:
				stopword_bins[word] = 1
ranks = sorted(stopword_bins.items(), key=itemgetter(1), reverse=True)
for item in ranks[:20]:
	print(item)

# Question 9
print()
print('Question 9')
word_bins = {}
for q in q_array:
	if 'download' in q['query'].lower().split():
		for word in q['query'].lower().split():
			if word not in stopwords and re.search('[a-z]', word) and word != 'download':
				if word in word_bins:
					word_bins[word] += 1
				else:
					word_bins[word] = 1
ranks = sorted(word_bins.items(), key=itemgetter(1), reverse=True)
for item in ranks[:20]:
	print(item)

# Question 12
print()
print('Question 12')
al_gore = 0
john_hopkins = 0
johns_hopkins = 0
for q in q_array:
	if 'al gore' in q['query'].lower():
		al_gore += 1
	if 'john hopkins' in q['query'].lower():
		john_hopkins += 1
	if 'johns hopkins' in q['query'].lower():
		johns_hopkins += 1
print('al_gore:', al_gore)
print('john_hopkins:', john_hopkins)
print('johns_hopkins:', johns_hopkins)
if al_gore > johns_hopkins:
	print('\"Al Gore\" occurs more than \"Johns Hopkins\"')
else:
	print('\"Johns Hopkins\" occurs more than \"Al Gore\"')
if john_hopkins > johns_hopkins:
	print('\"John Hopkins\" occurs more than \"Johns Hopkins\"')
else:
	print('\"Johns Hopkins\" occurs more than \"John Hopkins\"')

# Question 14
# List of surnames from
# http://www2.census.gov/topics/genealogy/1990surnames/dist.all.last
# List of first names from
# http://deron.meranda.us/data/census-derived-all-first.txt
# Originally also from census.gov
print()
print('Question 14')
names = {}
with open('firstnames.txt') as file:
	for line in file:
		names[line[:-1].lower()] = 1
with open('lastnames.txt') as file:
	for line in file:
		names[line[:-1].lower()] = 1
name_count = 0
for q in q_array:
	for word in q['query'].lower().split():
		if word in names:
			name_count += 1
			break
print('With names:', name_count, 'percent:', name_count/len(q_array))

# Question 16
print()
print('Question 16')
syntax_count = 0
for q in q_array:
	# Boolean operators
	if re.search('^.*[\+\-:\*\^~]+.*$', q['query']):
		syntax_count += 1
	elif 'OR' in q['query'] or 'AND' in q['query'] or 'NOT' in q['query']:
		syntax_count += 1
	elif re.search('^.*\".+\".*$', q['query']):
		syntax_count += 1
print('Using query syntax:', syntax_count, 'percent:', syntax_count/len(q_array))

# Question 18
print()
print('Question 18')
time_dist = {9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0}
for q in q_array:
	hour = int(q['stamp'].hour)
	time_dist[hour] += 1
for time, count in sorted(time_dist.items()):
	print('Hour:', time, 'Count:', count, 'Percent:', count/len(q_array))