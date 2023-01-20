import constants
from helpers import read_from_file
from math import log
from constants import NER_TAGS
from conllu import TokenList


# sentence as a list of strings
def baseline_decode(sentence_list, emissions_probabilities):

	result_tags = []

	for word in sentence_list:
		if word in emissions_probabilities:
			temp_prob = constants.MIN_FLOAT
			temp_tag = ""
			for tag in NER_TAGS:
				if log(emissions_probabilities[word][tag]) > temp_prob:
					temp_prob = log(emissions_probabilities[word][tag])
					temp_tag = tag
			result_tags.append(temp_tag)
		else:
			result_tags.append("B-MISC")

	result = TokenList([])

	for index, word in enumerate(sentence_list):
		# populate TokenList
		result.append({'id': index, 'form': word, 'tag': result_tags[index]})

	return result
