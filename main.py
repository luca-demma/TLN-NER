from conllu import parse
from enum import Enum
import constants
from helpers import write_to_file, multi_dict


with open(constants.IT_TRAIN_PATH) as f:
	train_text = f.read()
	sentences = parse(train_text, fields=["id", "form", "tag"])


class NerTagExtended(Enum):
	START = "START"
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

for w in emissions_counts.keys():
	for t in emissions_counts[w].keys():
		w_count = 0
		for tt in emissions_counts[w].keys():
			w_count += int(emissions_counts[w][tt])
		emissions_probabilities[w][t] = emissions_counts[w][t] / w_count

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
	for t in transitions_counts[w].keys():
		w_count = 0
		for tt in transitions_counts[w].keys():
			w_count += int(transitions_counts[w][tt])
		transitions_probabilities[w][t] = transitions_counts[w][t] / w_count

write_to_file(transitions_probabilities, 'transitions_probabilities')

