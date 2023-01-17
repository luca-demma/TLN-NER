from conllu import parse
import constants
from helpers import write_to_file, multi_dict, read_from_file
from math import log
from constants import NerTag
import sys


transitions_probabilities = read_from_file('transitions_probabilities')
emissions_probabilities = read_from_file('emissions_probabilities')


# VITERBI    DECODING

sentence_to_decode = "La vera casa di Harry Potter è il castello di Hogwarts"

sentence_to_decode_list = sentence_to_decode.split(" ")

# [tag][time_step]
viterbi_matrix = multi_dict(2, float)

# [tag][time_step]
backpointers = multi_dict(2, float)

# init
for t in NerTag:
	viterbi_matrix[t.value][0] = transitions_probabilities['START'][t.value] * emissions_probabilities[sentence_to_decode_list[0]][t.value]
	backpointers[t.value][0] = 0

# recursion    index == time_stamp
for time_stamp, w in enumerate(sentence_to_decode_list):
	# starting from the second word because the first word was processed by the init already
	if time_stamp > 0:
		for t in NerTag:
			temp_prob = 0
			for tt in NerTag:
				temp_prob = max(
					viterbi_matrix[tt.value][time_stamp - 1] * transitions_probabilities[tt.value][t.value] * emissions_probabilities[w][t.value],
					temp_prob
				)
			viterbi_matrix[t.value][time_stamp] = temp_prob
			backpointers[t.value][time_stamp] = temp_prob

# Termination Step
best_path_prob = 0

for t in NerTag:
	best_path_prob = max(best_path_prob, viterbi_matrix[t.value][len(sentence_to_decode_list) - 1])

best_path_pointer = best_path_prob

write_to_file(viterbi_matrix, "VITERBI_TEST")
write_to_file(backpointers, "BACKPOINTERS_TEST")
print("BEST_PATH_PROB " + str(best_path_prob))
print("BEST_PATH_POINTER " + str(best_path_pointer))

for index, w in enumerate(sentence_to_decode_list):
	max_tag = ""
	for tag in NerTag:
		max_tag = tag.value if viterbi_matrix[tag.value][index] > viterbi_matrix[max_tag][index] else max_tag
	print(w + " => " + max_tag)

