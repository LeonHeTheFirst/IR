import os, random, json, csv
import numpy as np
from pprint import pprint

# function to read in the training data and create large documents for each region
def read_training(filename):
	with open(filename) as json_file:
		data = json.load(json_file)
	regions = {}
	for recipe in data:
		if recipe['cuisine'] in regions:
			regions[recipe['cuisine']] += ' ' + ' '.join(recipe['ingredients']).lower()
		else:
			regions[recipe['cuisine']] = ' '.join(recipe['ingredients']).lower()
	# pprint(regions)
	return regions

regions = read_training('cuisine.train.json')

print(regions['russian'])