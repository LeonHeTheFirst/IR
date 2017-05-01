import os, random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

# reference: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
# function to read in the training data
def read_book_training(language):
	label_array = []
	data_array = []
	start_book = 0
	end_book = 0
	if language == 'en':
		with open('en.train.utf8') as book_file:
			start_str = 'END THE SMALL PRINT!'
			for index, line in enumerate(book_file):
				if start_book == 1 and end_book == 0:
					data_array.append(line)
					label_array.append(0)
				if start_str in line:
					start_book = 1
	elif language == 'fr':
		with open('fr.train.utf8') as book_file:
			start_str = 'START OF THE PROJECT GUTENBERG EBOOK'
			end_str = 'Small Print'
			for index, line in enumerate(book_file):
				if start_book == 1 and end_book == 0:
					data_array.append(line)
					label_array.append(1)
				if start_str in line:
					start_book = 1
				if end_str in line:
					end_book = 1
	elif language == 'es':
		start_str = '*END*THE SMALL PRINT!'
		with open('es.train.utf8') as book_file:
			for index, line in enumerate(book_file):
				if start_book == 1 and end_book == 0:
					data_array.append(line)
					label_array.append(2)
				if start_str in line:
					start_book = 1
	else:
		print('wrong language')
	return label_array, data_array

# function to read in the test data
def read_book_testing(language):
	data_array = []
	label_array = []
	if language == 'en':
		with open('en.test.utf8') as book_file:
			for line in book_file:
				data_array.append(line)
				label_array.append(0)
	elif language == 'fr':
		with open('fr.test.utf8') as book_file:
			for line in book_file:
				data_array.append(line)
				label_array.append(1)
	elif language == 'es':
		with open('es.test.utf8') as book_file:
			for line in book_file:
				data_array.append(line)
				label_array.append(2)
	else:
		print('wrong language')
	return label_array, data_array

# read in the training data
labels_en, data_en = read_book_training('en')
labels_fr, data_fr = read_book_training('fr')
labels_es, data_es = read_book_training('es')

# combine languages into single training set
labels = labels_en + labels_fr + labels_es
data = data_en + data_fr + data_es

#randomize the training data
zipped = list(zip(labels, data))
random.shuffle(zipped)
labels, data = zip(*zipped)

# read in the test data
test_labels_en, test_data_en = read_book_testing('en')
test_labels_fr, test_data_fr = read_book_testing('fr')
test_labels_es, test_data_es = read_book_testing('es')

# combine test data
test_labels = test_labels_en + test_labels_fr + test_labels_es
test_data = test_data_en + test_data_fr + test_data_es

# train and predict using binary counts and svm
pipe_svm = Pipeline([
	('vectorizer', CountVectorizer()),
	('classifier', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3,
								 n_iter=5, random_state=42))])

pipe_svm.fit(data, labels)
answers_svm = pipe_svm.predict(test_data)

# find the total number of docs returned and number of relevant docs returned
matched_svm_en = 0
labelled_svm_en = 0
for classes, truth in zip(answers_svm, test_labels):
	if classes == 0:
		labelled_svm_en += 1
		if classes == truth:
			matched_svm_en += 1

matched_svm_fr = 0
labelled_svm_fr = 0
for classes, truth in zip(answers_svm, test_labels):
	if classes == 1:
		labelled_svm_fr += 1
		if classes == truth:
			matched_svm_fr += 1

matched_svm_es = 0
labelled_svm_es = 0
for classes, truth in zip(answers_svm, test_labels):
	if classes == 2:
		labelled_svm_es += 1
		if classes == truth:
			matched_svm_es += 1

# 1000 relevant docs for each language
relevant = 1000

# print results
print('English: ', matched_svm_en, relevant, labelled_svm_en)

# find precision, recall, and f_1 for all the methods
p_svm_en = matched_svm_en/labelled_svm_en
r_svm_en = matched_svm_en/relevant
f_svm_en = 2 * p_svm_en * r_svm_en / (p_svm_en + r_svm_en)

print('Calculated values: precision, recall, F_1')
print('svm: precision =', matched_svm_en, '/', labelled_svm_en, '=', p_svm_en)
print('svm: recall =', matched_svm_en, '/', relevant, '=', r_svm_en)
print('svm: F_1 = 2 *', p_svm_en, '*', r_svm_en, '/(', p_svm_en, '+', r_svm_en, ') =', f_svm_en)

print('French: ', matched_svm_fr, relevant, labelled_svm_fr)

# find precision, recall, and f_1 for all the methods
p_svm_fr = matched_svm_fr/labelled_svm_fr
r_svm_fr = matched_svm_fr/relevant
f_svm_fr = 2 * p_svm_fr * r_svm_fr / (p_svm_fr + r_svm_fr)

print('Calculated values: precision, recall, F_1')
print('svm: precision =', matched_svm_fr, '/', labelled_svm_fr, '=', p_svm_fr)
print('svm: recall =', matched_svm_fr, '/', relevant, '=', r_svm_fr)
print('svm: F_1 = 2 *', p_svm_fr, '*', r_svm_fr, '/(', p_svm_fr, '+', r_svm_fr, ') =', f_svm_fr)

print('Spanish: ', matched_svm_es, relevant, labelled_svm_es)

# find precision, recall, and f_1 for all the methods
p_svm_es = matched_svm_es/labelled_svm_es
r_svm_es = matched_svm_es/relevant
f_svm_es = 2 * p_svm_es * r_svm_es / (p_svm_es + r_svm_es)

print('Calculated values: precision, recall, F_1')
print('svm: precision =', matched_svm_es, '/', labelled_svm_es, '=', p_svm_es)
print('svm: recall =', matched_svm_es, '/', relevant, '=', r_svm_es)
print('svm: F_1 = 2 *', p_svm_es, '*', r_svm_es, '/(', p_svm_es, '+', r_svm_es, ') =', f_svm_es)

