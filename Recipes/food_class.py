import os, random, json, csv
from pprint import pprint
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import numpy as np

normalization_factor = 4000
vectorizer = 'count'
truncate = False
# reference: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
# function to read in the training data
def read_training(filename):
	with open(filename) as json_file:
		data = json.load(json_file)
	cuisine_dict = {}
	ingredient_dict = {}
	region_counts = {}
	for recipe in data:
		if recipe['cuisine'] in region_counts:
			region_counts[recipe['cuisine']] += 1
		else:
			region_counts[recipe['cuisine']] = 1
		if region_counts[recipe['cuisine']] < normalization_factor:
			cuisine_dict[recipe['id']] = recipe['cuisine']
			if not truncate:
				ingredient_dict[recipe['id']] = ' '.join(recipe['ingredients']).lower()
			# the following code only takes the last word of each ingredient
			# this decreases certainty in output and
			# makes cuisines across region appear more similar
			else:
				simplified_ingredients = ''
				for ingredient in recipe['ingredients']:
					last_word = ingredient.rsplit(' ', 1)[-1].lower()
					simplified_ingredients += last_word + ' '
				ingredient_dict[recipe['id']] = simplified_ingredients
	# pprint(cuisine_dict)
	return cuisine_dict, ingredient_dict

def read_testing(testname, solutionname):
	with open(testname) as json_file:
		data_test = json.load(json_file)

	cuisine_dict = {}
	with open(solutionname) as csv_file:
		csv_f = csv.reader(csv_file)
		for line in csv_f:
			cuisine_dict[int(line[0])] = line[1]

	ingredient_dict = {}
	for recipe in data_test:
		ingredient_dict[recipe['id']] = ' '.join(recipe['ingredients']).lower()
	# pprint(cuisine_dict)
	return cuisine_dict, ingredient_dict

# function to read in the training data and create large documents for each region
def get_regions(filename):
	with open(filename) as json_file:
		data = json.load(json_file)
	regions = {}
	region_counts = {}
	for recipe in data:
		if recipe['cuisine'] in regions:
			regions[recipe['cuisine']] += ' ' + ' '.join(recipe['ingredients']).lower()
			region_counts[recipe['cuisine']] += 1
		else:
			regions[recipe['cuisine']] = ' '.join(recipe['ingredients']).lower()
			region_counts[recipe['cuisine']] = 1
	# pprint(regions)
	# print(region_counts)
	return regions, region_counts

def sort_probs(predict_probs, n):
	top_n_lists = []
	prob_lists = []
	for prob_list in predict_probs:
		classes = []
		probs = []
		top_n_indices = np.argsort(prob_list)[-n:][::-1]
		for x in range(0,n):
			classes.append(label_map[top_n_indices[x]])
			probs.append(prob_list[top_n_indices[x]])
		# print(classes)
		# print(probs)
		top_n_lists.append(classes)
		prob_lists.append(probs)
	return top_n_lists, prob_lists

regions, region_counts = get_regions('cuisine.train.json')
region_names = []
region_data = []
# i = 0
for k, v in regions.items():
	region_names.append(k)
	region_data.append(v)
# read in the training data
train_labels, train_data = read_training('cuisine.train.json')

# read in the test data
test_labels, test_data = read_testing('cuisine.test.json', 'cuisine.solution.csv')
# format test data
test_array = []
test_ids = []
# i = 0
for k, v in test_data.items():
	test_array.append(v)
	test_ids.append(k)
# format truth data
truth_array = []
for k, v in test_labels.items():
	truth_array.append(v)
# map cuisine labels to ints
label_map = {}
label_int = 0
for cuisine in train_labels.values():
	if cuisine not in label_map:
		label_map[cuisine] = label_int
		label_map[label_int] = cuisine
		label_int += 1
# pprint(label_map)
for k, v in train_labels.items():
	train_labels[k] = label_map[v]

# train and predict using Tfidf counts and svm
if vectorizer == 'count':
	pipe_svm = Pipeline([
		('vectorizer', CountVectorizer()),
		('classifier', SGDClassifier(loss='log', penalty='l2', alpha=1e-3,
									 n_iter=5, random_state=42))])
elif vectorizer == 'tfidf':
	pipe_svm = Pipeline([
		('vectorizer', TfidfVectorizer()),
		('classifier', SGDClassifier(loss='log', penalty='l2', alpha=1e-3,
									 n_iter=5, random_state=42))])

training_data = []
training_labels = []
for data, label in zip(train_data.values(), train_labels.values()):
	training_data.append(data)
	training_labels.append(label)
print('len of data:' , len(training_data))
print('len of labels:' , len(training_labels))

# for data, label in zip(training_data, training_labels):
# 	print(label, ':', data[:40])
# print(train_labels.values())
pipe_svm.fit(training_data, training_labels)
answers_svm = pipe_svm.predict_proba(test_array)
region_compare = pipe_svm.predict_proba(region_data)
# pprint(answers_svm)

# sort the probability arrays and tie them to classes
# top_n = 1
# top_n_lists = []
# prob_lists = []
# for prob_list in answers_svm:
# 	classes = []
# 	probs = []
# 	top_n_indices = np.argsort(prob_list)[-top_n:][::-1]
# 	for x in range(0,top_n):
# 		classes.append(label_map[top_n_indices[x]])
# 		probs.append(prob_list[top_n_indices[x]])
# 	# print(classes)
# 	# print(probs)
# 	top_n_lists.append(classes)
# 	prob_lists.append(probs)
top_n_lists, prob_lists = sort_probs(answers_svm, 1)
region_lists, region_probs = sort_probs(region_compare, 20)
# find the total number of docs returned and number of relevant docs returned
matched_svm = 0
not_matched = 0
i = 0
for classes, recipe_id in zip(top_n_lists, test_ids):
	if test_labels[recipe_id] in classes:
		matched_svm += 1
	else:
		not_matched += 1
		# print('not matched:', classes, prob_lists[i], test_ids[i], test_labels[recipe_id], test_array[i])
	i+=1
for region_name, classes, probs in sorted(zip(region_names, region_lists, region_probs)):
	print('\n' + region_name + ':')
	for reg, prob in zip(classes, probs):
		print(reg, prob)

# print results
print('Matched: ', matched_svm)
print('Not Matched:', not_matched)

# for region, count in region_counts.items():
# 	print(region, ':', count)
