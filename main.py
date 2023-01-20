from helpers import from_conllu_to_sentences, string_to_csv, read_from_file
import constants
from decode import decode
from baseline import baseline_decode
from tqdm import tqdm
import sys

# Command line argument to set to calculate the baseline
BASELINE = ""
if len(sys.argv) > 2:
	BASELINE = sys.argv[2]

LANG = 'IT'
if len(sys.argv) > 1:
	LANG = sys.argv[1]

# Read TEST sentences
if LANG == 'IT':
	sentences = from_conllu_to_sentences(constants.IT_TEST_PATH)
elif LANG == 'EN':
	sentences = from_conllu_to_sentences(constants.EN_TEST_PATH)
else:
	raise Exception("LANG parameter can be only IT or EN (case sensitive)")


def decode_sentence(sentence, transitions_probabilities, emissions_probabilities):
	word_list = []
	for word in sentence:
		word_list.append(word['form'])

	if BASELINE == "baseline":
		sentence_decoded = baseline_decode(word_list, emissions_probabilities)
	else:
		sentence_decoded = decode(word_list, transitions_probabilities, emissions_probabilities)

	csv_sentence = ""
	# Creating the csv for result comparison
	for index, token in enumerate(sentence):
		sd_token = sentence_decoded[index]
		is_correct = "yes" if token['tag'] == sd_token['tag'] else "no"
		csv_sentence += str(token['id']) + '\t' + token['form'] + '\t' + token['tag'] + '\t' + sd_token['tag'] + '\t' + is_correct + '\n'

	# End of sentence
	csv_sentence += '\n'
	return csv_sentence


# Read probabilities matrixes from file
transitions_probabilities = read_from_file('LEARNING/' + LANG + '/transitions_probabilities')
emissions_probabilities = read_from_file('LEARNING/' + LANG + '/emissions_probabilities')

# List of csv strings representing a single sentence
csv_sentences = []

# Decode every sentence
for s in tqdm(sentences, desc="DECODING..."):
	csv_sentences.append(decode_sentence(s, transitions_probabilities, emissions_probabilities))

# Write the result to a CSV
results_csv = 'ID\tWord\tTAG_Test\tTAG_Calculated\tIS_Correct\n'

for s in csv_sentences:
	results_csv += s

string_to_csv("DECODING/" + LANG + "/" + LANG + BASELINE + "_results_comparison", results_csv)
