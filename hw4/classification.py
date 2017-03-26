import os
import csv
import pandas as pd
from pandas import DataFrame
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

# reference: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
# function to read in the test data
def read_tsv(path):
	label_array = []
	data_array = []
	with open(path) as tsv_file:
		tsv = csv.reader(tsv_file, delimiter='\t')
		for index, line in enumerate(tsv):
			label_array.append(line[0])
			if int(line[0]) == 1:
				print(line[2])
			try:
				data_array.append(line[8])
			except:
				print('exception', index)
	return label_array, data_array

# function to read in the training data and format it for sklearn
def dataframe_tsv(path):
	cols = ['class', 'title', 'abstract']
	table = pd.read_csv(path, sep='\t', usecols=[0, 2, 8], names=cols)
	return table

# read in the training data
data = dataframe_tsv('phase1.train.shuf.tsv')

# combine title and abstract
data['text'] = data['title'] + data['abstract']
# read in the test data
test_labels, test_data = read_tsv('phase1.test.shuf.tsv')

# train and predict using binary counts and svm
print('svm count')
pipe_svm = Pipeline([
	('vectorizer', CountVectorizer()),
	('classifier', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3,
								 n_iter=5, random_state=42))])

pipe_svm.fit(data['text'].values.astype(str), data['class'].values)
answers_svm = pipe_svm.predict(test_data)

# train and predict using binary counts, with ngrams, and svm
print('svm count ngram')
pipe_svm_ngram = Pipeline([
	('vectorizer', CountVectorizer(ngram_range=(1, 2))),
	('classifier', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3,
								 n_iter=5, random_state=42))])

pipe_svm_ngram.fit(data['text'].values.astype(str), data['class'].values)
answers_svm_ngram = pipe_svm_ngram.predict(test_data)

# train and predict using tfidf and svm
print('svm tfidf')
pipe_svm_tfidf = Pipeline([
	('vectorizer', TfidfVectorizer()),
	('classifier', SGDClassifier())])

pipe_svm_tfidf.fit(data['text'].values.astype(str), data['class'].values)
answers_svm_tfidf = pipe_svm_tfidf.predict(test_data)

# train and predict using binary counts and naive bayes
print('nb')
pipe_nb = Pipeline([
	('vectorizer', CountVectorizer()),
	('classifier', MultinomialNB())])

pipe_nb.fit(data['text'].values.astype(str), data['class'].values)
answers_nb = pipe_nb.predict(test_data)

# train and predict using tfidf and nearest neighbor
print('nn')
pipe_nn = Pipeline([
	('vectorizer', TfidfVectorizer()),
	('classifier', KNeighborsClassifier())])

pipe_nn.fit(data['text'].values.astype(str), data['class'].values)
answers_nn = pipe_nn.predict(test_data)

# find the total number of docs returned and number of relevant docs returned
matched_svm = 0
labelled_svm = 0
for i, classes in zip(answers_svm, test_labels):
	if i == 1:
		labelled_svm += 1
	if i == int(classes) and i == 1:
		matched_svm += 1

# find the total number of docs returned and number of relevant docs returned
matched_svm_ngram = 0
labelled_svm_ngram = 0
for i, classes in zip(answers_svm_ngram, test_labels):
	if i == 1:
		labelled_svm_ngram += 1
	if i == int(classes) and i == 1:
		matched_svm_ngram += 1

# find the total number of docs returned and number of relevant docs returned
matched_svm_tfidf = 0
labelled_svm_tfidf = 0
for i, classes in zip(answers_svm_tfidf, test_labels):
	if i == 1:
		labelled_svm_tfidf += 1
	if i == int(classes) and i == 1:
		matched_svm_tfidf += 1

# find the total number of docs returned and number of relevant docs returned
matched_nb = 0
labelled_nb = 0
for i, classes in zip(answers_nb, test_labels):
	if i == 1:
		labelled_nb += 1
	if i == int(classes) and i == 1:
		matched_nb += 1

# find the total number of docs returned and number of relevant docs returned
matched_nn = 0
labelled_nn = 0
for i, classes in zip(answers_nn, test_labels):
	if i == 1:
		labelled_nn += 1
	if i == int(classes) and i == 1:
		matched_nn += 1

# find total relevant documents
relevant = 0
for i in test_labels:
	if int(i) == 1:
		relevant += 1

# print results
print('svm: ', matched_svm, relevant, labelled_svm)
print('svm ngram: ', matched_svm_ngram, relevant, labelled_svm_ngram)
print('svm tfidf: ', matched_svm_tfidf, relevant, labelled_svm_tfidf)
print('nb : ', matched_nb, relevant, labelled_nb)
print('nn : ', matched_nn, relevant, labelled_nn)

# find precision, recall, and f_1 for all the methods
p_svm = matched_svm/labelled_svm
r_svm = matched_svm/relevant
f_svm = 2 * p_svm * r_svm / (p_svm + r_svm)

p_svm_ngram = matched_svm_ngram/labelled_svm_ngram
r_svm_ngram = matched_svm_ngram/relevant
f_svm_ngram = 2 * p_svm_ngram * r_svm_ngram / (p_svm_ngram + r_svm_ngram)

p_svm_tfidf = matched_svm_tfidf/labelled_svm_tfidf
r_svm_tfidf = matched_svm_tfidf/relevant
f_svm_tfidf = 2 * p_svm_tfidf * r_svm_tfidf / (p_svm_tfidf + r_svm_tfidf)

p_nb = matched_nb/labelled_nb
r_nb = matched_nb/relevant
f_nb = 2 * p_nb * r_nb / (p_nb + r_nb)

p_nn = matched_nn/labelled_nn
r_nn = matched_nn/relevant
f_nn = 2 * p_nn * r_nn / (p_nn + r_nn)

print('Calculated values: precision, recall, F_1')
print('svm: precision =', matched_svm, '/', labelled_svm, '=', p_svm)
print('svm: recall =', matched_svm, '/', relevant, '=', r_svm)
print('svm: F_1 = 2 *', p_svm, '*', r_svm, '/(', p_svm, '+', r_svm, ') =', f_svm)

print('svm_ngram: precision =', matched_svm_ngram, '/', labelled_svm_ngram, '=', p_svm_ngram)
print('svm_ngram: recall =', matched_svm_ngram, '/', relevant, '=', r_svm_ngram)
print('svm_ngram: F_1 = 2 *', p_svm_ngram, '*', r_svm_ngram, '/(', p_svm_ngram, '+', r_svm_ngram, ') =', f_svm_ngram)

print('svm_tfidf: precision =', matched_svm_tfidf, '/', labelled_svm_tfidf, '=', p_svm_tfidf)
print('svm_tfidf: recall =', matched_svm_tfidf, '/', relevant, '=', r_svm_tfidf)
print('svm_tfidf: F_1 = 2 *', p_svm_tfidf, '*', r_svm_tfidf, '/(', p_svm_tfidf, '+', r_svm_tfidf, ') =', f_svm_tfidf)

print('nb: precision =', matched_nb, '/', labelled_nb, '=', p_nb)
print('nb: recall =', matched_nb, '/', relevant, '=', r_nb)
print('nb: F_1 = 2 *', p_nb, '*', r_nb, '/(', p_nb, '+', r_nb, ') =', f_nb)

print('nn: precision =', matched_nn, '/', labelled_nn, '=', p_nn)
print('nn: recall =', matched_nn, '/', relevant, '=', r_nn)
print('nn: F_1 = 2 *', p_nn, '*', r_nn, '/(', p_nn, '+', r_nn, ') =', f_nn)

