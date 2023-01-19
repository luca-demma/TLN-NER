import constants
from helpers import write_to_file, multi_dict, from_conllu_to_sentences
from constants import NerTag
from tqdm import tqdm


print("Started LEARNING")


sentences = from_conllu_to_sentences(constants.IT_TRAIN_PATH)

# [word][tag]
emissions_counts = multi_dict(2, int)

for s in tqdm(sentences, desc="Emissions => Counting"):
	for token in s:
		emissions_counts[token['form']][token['tag']] += 1

write_to_file(emissions_counts, 'emissions_count')


# [word][tag]
emissions_probabilities = multi_dict(2, float)

# for every word found
for word in tqdm(emissions_counts.keys(), desc="Emissions => Calculating Probabilities"):
	for tag in NerTag:
		# Total count of word
		w_count = 0
		for tt in NerTag:
			# +1 used for the pseudocounting
			w_count += int(emissions_counts[word][tt.value]) + 1
		# we use + 1 to give a very low probability to the pair word/tag instead of giving
		# 0 probability that will set to zero the total probability calculated
		emissions_probabilities[word][tag.value] = (emissions_counts[word][tag.value] + 1) / w_count

# Write emission probabilities to file as csv and pickle
write_to_file(emissions_probabilities, 'emissions_probabilities', True)


# [prev_tag][tag]
transitions_counts = multi_dict(2, int)

for s in tqdm(sentences, desc="Transitions => Counting"):
	for token in s:
		prev_tag = "START" if token['id'] == 0 else s[token['id'] - 1]['tag']
		transitions_counts[prev_tag][token['tag']] += 1


write_to_file(transitions_counts, 'transitions_counts')


transitions_probabilities = multi_dict(2, float)

for word in tqdm(transitions_counts.keys(), desc="Transitions => Calculating Probabilities"):
	for tag in NerTag:
		# Total count of word
		w_count = 0
		for tt in NerTag:
			# +1 used for pseudocounting (look at emissions calc)
			w_count += int(transitions_counts[word][tt.value]) + 1
		# +1 used for pseudocounting (look at emissions calc)
		transitions_probabilities[word][tag.value] = (transitions_counts[word][tag.value] + 1) / w_count


# Write transitions probabilities to file as csv and pickle
write_to_file(transitions_probabilities, 'transitions_probabilities', True)
