import pandas as pd

import constants
from helpers import multi_dict, read_from_file
from math import log
from constants import NER_TAGS
from conllu import TokenList


def decode(sentence_list, transitions_probabilities, emissions_probabilities):

	# [tag][time_step]
	viterbi_matrix = multi_dict(2, float)

	# [tag][time_step]
	backpointers = multi_dict(2, str)

	# INIT step
	for tag in NER_TAGS:
		# smoothing uniforme
		emission_probability = 1/len(NER_TAGS) if emissions_probabilities[sentence_list[0]][tag] == 0 else emissions_probabilities[sentence_list[0]][tag]
		viterbi_matrix[tag][0] = log(transitions_probabilities['START'][tag]) + log(emission_probability)
		backpointers[tag][0] = tag

	# RECURSION step
	for time_step, word in enumerate(sentence_list):
		# starting from the second word because the first word was processed by the init already
		if time_step > 0:
			for tag in NER_TAGS:
				temp_prob = constants.MIN_FLOAT

				# the tag that in the prob calculus gave the maximum , used for the backpointer
				argmax = ""

				# smoothing uniforme
				emission_probability = 1 / len(NER_TAGS) if emissions_probabilities[word][tag] == 0 else emissions_probabilities[word][tag]

				for tt in NER_TAGS:
					if viterbi_matrix[tt][time_step - 1] + log(transitions_probabilities[tt][tag]) + log(emission_probability) > temp_prob:
						temp_prob = viterbi_matrix[tt][time_step - 1] + log(transitions_probabilities[tt][tag]) + log(emission_probability)
						argmax = tt

				viterbi_matrix[tag][time_step] = temp_prob
				backpointers[tag][time_step] = argmax

	# TERMINATION Step
	best_path_prob = constants.MIN_FLOAT
	best_path_prob_argmax = ""

	for tag in NER_TAGS:
		if viterbi_matrix[tag][len(sentence_list) - 1] > best_path_prob:
			best_path_prob = viterbi_matrix[tag][len(sentence_list) - 1]
			best_path_prob_argmax = tag

	result_tags = [best_path_prob_argmax]

	# visitiamo la matrice backpointer all'inverso per trovare il path di NER tag che ha generato la probablità maggiore
	def backpointing(back_tag, back_time_step):
		if back_time_step >= 1:
			new_back_tag = backpointers[back_tag][back_time_step]
			result_tags.append(new_back_tag)
			backpointing(new_back_tag, back_time_step - 1)

	backpointing(best_path_prob_argmax, len(sentence_list) - 1)

	# i risultati sono in ordine inverso, gli ordiniamo semplicemente eseguendo la reverse
	result_tags.reverse()

	# DEBUGGING
	if False:
		pd.set_option('display.max_columns', None)
		print("aaaaa " + str(len(sentence_list) - 1))
		print("bbbbb " + str(best_path_prob))
		print("ccccc " + best_path_prob_argmax)
		print(pd.DataFrame(viterbi_matrix))
		print(pd.DataFrame(backpointers))
		print(result_tags)


	result = TokenList([])

	for index, word in enumerate(sentence_list):
		max_tag = max(viterbi_matrix, key=lambda tag: viterbi_matrix[tag][index])
		# populate TokenList
		result.append({'id': index, 'form': word, 'tag': result_tags[index]})

	return result



#############################################
# Test sentences from slide #
#############################################

# Read probabilities matrixes from file
if __name__ == "__main__":
	transitions_probabilities = read_from_file('LEARNING/IT/transitions_probabilities')
	emissions_probabilities = read_from_file('LEARNING/IT/emissions_probabilities')

	for s in constants.TEST_SENTENCES:
		result = decode(s, transitions_probabilities, emissions_probabilities)
		print("_______________________________________")
		for token in result:
			print(str(token['id']) + '\t' + token['form'] + '\t' + token['tag'])
