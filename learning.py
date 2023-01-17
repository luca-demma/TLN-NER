import constants
from conllu import parse
from helpers import write_to_file, multi_dict, from_conllu_to_sentences
from constants import NerTag


sentences = from_conllu_to_sentences(constants.IT_TRAIN_PATH)

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
