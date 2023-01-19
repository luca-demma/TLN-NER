import constants
from helpers import write_to_file, multi_dict, read_from_file
from math import log
from constants import NER_TAGS
from conllu import TokenList

# VITERBI    DECODING
sentence_to_decode = "Si stabilì ad Amburgo per la sua ammirazione nei confronti della letteratura tedesca ( aveva imparato la lingua in carcere ) , specialmente per i romantici come Novalis e Hölderlin ."
# sentence_to_decode = "Mr Dursley era direttore di una ditta di nome Grunnings , che fabbricava trapani in Italia ."

sentence_to_decode_list = sentence_to_decode.split(" ")


def decode(sentence_list):

	# [tag][time_step]
	viterbi_matrix = multi_dict(2, float)

	# Read probabilities matrixes from file
	transitions_probabilities = read_from_file('transitions_probabilities')
	emissions_probabilities = read_from_file('emissions_probabilities')

	# INIT step
	for tag in NER_TAGS:
		# smoothing uniforme
		emission_probability = 1/len(NER_TAGS) if emissions_probabilities[sentence_list[0]][tag] == 0 else emissions_probabilities[sentence_list[0]][tag]
		viterbi_matrix[tag][0] = log(transitions_probabilities['START'][tag]) + log(emission_probability)

	# RECURSION step
	for time_stamp, word in enumerate(sentence_list):
		# starting from the second word because the first word was processed by the init already
		if time_stamp > 0:
			for tag in NER_TAGS:
				temp_prob = constants.MIN_FLOAT
				# smoothing uniforme
				emission_probability = 1 / len(NER_TAGS) if emissions_probabilities[word][tag] == 0 else emissions_probabilities[word][tag]
				for tt in NER_TAGS:
					temp_prob = max(
						viterbi_matrix[tt][time_stamp - 1] + log(transitions_probabilities[tt][tag]) + log(emission_probability),
						temp_prob
					)
				viterbi_matrix[tag][time_stamp] = temp_prob

	# TERMINATION Step
	best_path_prob = constants.MIN_FLOAT

	for tag in NER_TAGS:
		best_path_prob = max(best_path_prob, viterbi_matrix[tag][len(sentence_list) - 1])


	# write_to_file(viterbi_matrix, "VITERBI_OUTPUT")
	# print("BEST_PATH_PROB " + str(best_path_prob))

	result = TokenList([])

	for index, word in enumerate(sentence_list):
		max_tag = max(viterbi_matrix, key=lambda tag: viterbi_matrix[tag][index])
		# populate TokenList
		result.append({'id': index, 'form': word, 'tag': max_tag})

	return result
