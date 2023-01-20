import constants
from helpers import write_to_file, multi_dict, from_conllu_to_sentences
from constants import NER_TAGS
from tqdm import tqdm
import sys

# Command line argument to set the language // DEFAULT IT
LANG = 'IT'
if len(sys.argv) > 1:
	LANG = sys.argv[1]

print("Started LEARNING. LANG: " + LANG)

# Reading TRAIN sentences
if LANG == 'IT':
	sentences = from_conllu_to_sentences(constants.IT_TRAIN_PATH)
elif LANG == 'EN':
	sentences = from_conllu_to_sentences(constants.EN_TRAIN_PATH)
else:
	raise Exception("LANG parameter can be only IT or EN (case sensitive)")

# [word][tag]
emissions_counts = multi_dict(2, int)

for s in tqdm(sentences, desc="Emissions => Counting"):
	for token in s:
		emissions_counts[token['form']][token['tag']] += 1

# Write Emissions count to CSV file
write_to_file(emissions_counts, 'LEARNING/' + LANG + '/emissions_count')


# [word][tag]
emissions_probabilities = multi_dict(2, float)

# for every word found
for word in tqdm(emissions_counts.keys(), desc="Emissions => Calculating Probabilities"):
	for tag in NER_TAGS:
		# Total count of word
		w_count = 0
		for tt in NER_TAGS:
			# +1 used for the pseudocounting
			w_count += int(emissions_counts[word][tt]) + 1
		# we use + 1 to give a very low probability to the pair word/tag instead of giving
		# 0 probability that will set to zero the total probability calculated
		emissions_probabilities[word][tag] = (emissions_counts[word][tag] + 1) / w_count

# Write emission probabilities to file as CSV and pickle
write_to_file(emissions_probabilities, 'LEARNING/' + LANG + '/emissions_probabilities', True)


# [prev_tag][tag]
transitions_counts = multi_dict(2, int)

for s in tqdm(sentences, desc="Transitions => Counting"):
	for token in s:
		prev_tag = "START" if token['id'] == 0 else s[token['id'] - 1]['tag']
		transitions_counts[prev_tag][token['tag']] += 1

# Write Transitions count to CSV file
write_to_file(transitions_counts, 'LEARNING/' + LANG + '/transitions_counts')


transitions_probabilities = multi_dict(2, float)

for word in tqdm(transitions_counts.keys(), desc="Transitions => Calculating Probabilities"):
	for tag in NER_TAGS:
		# Total count of word
		w_count = 0
		for tt in NER_TAGS:
			# +1 used for pseudocounting (look at emissions calc)
			w_count += int(transitions_counts[word][tt]) + 1
		# +1 used for pseudocounting (look at emissions calc)
		transitions_probabilities[word][tag] = (transitions_counts[word][tag] + 1) / w_count


# Write Transitions probabilities to file as CSV and pickle
write_to_file(transitions_probabilities, 'LEARNING/' + LANG + '/transitions_probabilities', True)
