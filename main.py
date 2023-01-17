from conllu import parse
from enum import Enum
import constants
from helpers import write_to_file, multi_dict


with open(constants.IT_TRAIN_PATH) as f:
	train_text = f.read()
	sentences = parse(train_text, fields=["id", "form", "tag"])


class NerTag(Enum):
#	START = "START"
	B_PER = "B-PER"
	I_PER = "I-PER"
	B_ORG = "B-ORG"
	I_ORG = "I-ORG"
	B_LOC = "B-LOC"
	I_LOC = "I-LOC"
	B_MISC = "B-MISC"
	I_MISC = "I-MISC"
	OTHER = "O"


# [word][tag]
emissions_counts = multi_dict(2, int)

for s in sentences:
	for t in s:
		emissions_counts[t['form']][t['tag']] += 1

write_to_file(emissions_counts, 'emissions_count')


# [word][tag]
emissions_probabilities = multi_dict(2, float)

# for evry word found
for w in emissions_counts.keys():
	for t in NerTag:
		w_count = 0
		for tt in NerTag:
			# +1 used for the pseudocounting
			w_count += int(emissions_counts[w][tt.value]) + 1
		# we use + 1 to give a very low probability to the couple word/tag instead of giving
		# 0 probability that will set to zero the total probability calculated
		emissions_probabilities[w][t.value] = (emissions_counts[w][t.value] + 1) / w_count

write_to_file(emissions_probabilities, 'emissions_probabilities')



# [prev_tag][tag]
transitions_counts = multi_dict(2, int)

for s in sentences:
	for t in s:
		prev_tag = "START" if t['id'] == 0 else s[t['id'] - 1]['tag']
		transitions_counts[prev_tag][t['tag']] += 1

write_to_file(transitions_counts, 'transitions_counts')


transitions_probabilities = multi_dict(2, float)

for w in transitions_counts.keys():
	for t in NerTag:
		w_count = 0
		for tt in NerTag:
			# +1 used for pseudocounting (look at emissions calc)
			w_count += int(transitions_counts[w][tt.value]) + 1
		# +1 used for pseudocounting (look at emissions calc)
		transitions_probabilities[w][t.value] = (transitions_counts[w][t.value] + 1) / w_count

write_to_file(transitions_probabilities, 'transitions_probabilities')



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

