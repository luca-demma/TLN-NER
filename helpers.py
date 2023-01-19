import pandas as pd
import constants
from collections import defaultdict
import dill as pickle
from conllu import parse


def write_to_file(dict_2d, file_name, to_pickle = False):
	df = pd.DataFrame(dict_2d)
	# df.to_csv(OUTPUT_PATH + 'ccc.csv', index=None)
	# df.to_excel(constants.OUTPUT_PATH + file_name + '.xlsx', na_rep=0, columns=df.columns)
	df.to_csv(constants.OUTPUT_PATH + file_name + '.csv')

	# Write To Pickle
	if to_pickle:
		with open(constants.OUTPUT_PATH + file_name + '.pickle', 'wb') as file:
			pickle.dump(dict_2d, file)


# Utility function to create dictionary
def multi_dict(K, type):
	if K == 1:
		return defaultdict(type)
	else:
		return defaultdict(lambda: multi_dict(K-1, type))


def read_from_file(file_name):
	with open(constants.OUTPUT_PATH + file_name + '.pickle', 'rb') as file:
		return pickle.load(file)


def from_conllu_to_sentences(file_path):
	with open(file_path) as f:
		text = f.read()
		return parse(text, fields=["id", "form", "tag"])


def string_to_csv(file_name, the_string):
	text_file = open(constants.OUTPUT_PATH + file_name + '.csv', "w")
	text_file.write(the_string)
	text_file.close()
