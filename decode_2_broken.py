import constants
from helpers import multi_dict, read_from_file
from math import log
from constants import NER_TAGS
from conllu import TokenList
import pandas as pd


def decode(sentence_list, transitions_probabilities, emissions_probabilities):
	# [index_tag][time_step]
	viterbi_matrix = multi_dict(2, float)

	# [index_tag][time_step]
	backpointer = multi_dict(2, int)

	# INIT step
	for s, tag in enumerate(NER_TAGS):
		# smoothing uniforme
		emission_probability = 1 / len(NER_TAGS) if emissions_probabilities[sentence_list[0]][tag] == 0 else emissions_probabilities[sentence_list[0]][tag]
		viterbi_matrix[s][0] = log(transitions_probabilities['START'][tag]) + log(emission_probability)
		backpointer[s][0] = -1

	# RECURSION step
	for time_step, word in enumerate(sentence_list):
		# starting from the second word because the first word was processed by the init already
		if time_step > 0:
			for s, tag in enumerate(NER_TAGS):
				max_value = constants.MIN_FLOAT
				arg_max_tag = ""
				# smoothing uniforme
				emission_probability = 1 / len(NER_TAGS) if emissions_probabilities[word][tag] == 0 else \
				emissions_probabilities[word][tag]
				for tt_i, tt in enumerate(NER_TAGS):
					value = viterbi_matrix[tt_i][time_step - 1] + log(transitions_probabilities[tt][tag]) + log(
						emission_probability)
					if value > max_value:
						max_value = value
						arg_max_tag = tt
				viterbi_matrix[s][time_step] = max_value
				backpointer[s][time_step] = NER_TAGS.index(arg_max_tag)

	# TERMINATION Step

	best_path_prob = constants.MIN_FLOAT
	best_path_pointer = -1

	for i, tag in enumerate(NER_TAGS):
		if viterbi_matrix[i][len(sentence_list) - 1] > best_path_prob:
			best_path_prob = viterbi_matrix[i][len(sentence_list) - 1]
			best_path_pointer = i

	tags_list = []

	def recurs(time_stepp, indexx):
		if time_stepp >= 0:
			tags_list.append(constants.NER_TAGS[backpointer[indexx][time_stepp+1]])
			recurs(time_stepp-1, backpointer[indexx][time_stepp+1])

	recurs(len(sentence_list), best_path_pointer)

	tags_list.reverse()

	if False:
		pd.set_option('display.max_columns', None)
		print(pd.DataFrame(viterbi_matrix))
		print(pd.DataFrame(backpointer))
		print(best_path_prob)
		print(sentence_list)
		print(tags_list)


	# write_to_file(viterbi_matrix, "VITERBI_OUTPUT")
	# print("BEST_PATH_PROB " + str(best_path_prob))

	result = TokenList([])

	#max_tag = max(viterbi_matrix, key=lambda tag: viterbi_matrix[tag][len(sentence_list) - 1])

	#for index, word in enumerate(sentence_list):
		#max_tag = max(viterbi_matrix, key=lambda tag: viterbi_matrix[tag][index])
		# populate TokenList
		#result.append({'id': index, 'form': word, 'tag': max_tag})

	for index, word in enumerate(sentence_list):
		result.append({'id': index, 'form': word, 'tag': tags_list[index]})

	return result


#############################################
# Test sentences from slide #
#############################################

# Read probabilities matrixes from file
if __name__ == "__main__":
	transitions_probabilities = read_from_file('LEARNING/IT/transitions_probabilities')
	emissions_probabilities = read_from_file('LEARNING/IT/emissions_probabilities')

	for sentence in constants.TEST_SENTENCES:
		result = decode(sentence, transitions_probabilities, emissions_probabilities)
		print("_______________________________________")
		for token in result:
			print(str(token['id']) + '\t' + token['form'] + '\t' + token['tag'])
