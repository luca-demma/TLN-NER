from conllu import parse
from enum import Enum
from collections import defaultdict
import constants
from write_to_excel import write_to_excel

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


# Utility function to create dictionary
def multi_dict(K, type):
	if K == 1:
		return defaultdict(type)
	else:
		return defaultdict(lambda: multi_dict(K-1, type))


# [tag][word]
emissions_counts = multi_dict(2, int)

for s in sentences:
	for t in s:
		emissions_counts[t['tag']][t['form']] += 1

write_to_excel(emissions_counts, 'emissions_count')


emissions_probabilities = multi_dict(2, float)

for t in emissions_counts.keys():
	for w in emissions_counts[t].keys():
		w_count = 0
		for tt in emissions_counts.keys():
			w_count += int(emissions_counts[tt][w])
		emissions_probabilities[t][w] = emissions_counts[t][w] / w_count

write_to_excel(emissions_probabilities, 'emissions_probabilities')


# [tag][prev_tag]
transitions_counts = multi_dict(2, int)

for s in sentences:
	for t in s:
		prev_tag = "START" if t['id'] == 0 else s[t['id'] - 1]['tag']
		transitions_counts[t['tag']][prev_tag] += 1

write_to_excel(transitions_counts, 'transitions_counts')


transitions_probabilities = multi_dict(2, float)

for t in transitions_counts.keys():
	for w in transitions_counts[t].keys():
		w_count = 0
		for tt in transitions_counts.keys():
			w_count += int(transitions_counts[tt][w])
		transitions_probabilities[t][w] = transitions_counts[t][w] / w_count

write_to_excel(transitions_probabilities, 'transitions_probabilities')

