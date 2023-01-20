from helpers import from_conllu_to_sentences, string_to_csv
import constants
from decode import decode
from baseline import baseline_decode
from pqdm.processes import pqdm

# Read Sentences from conllu test file
sentences_raw = from_conllu_to_sentences(constants.IT_TEST_PATH)

# Needed for PQDM (just converting the conllu.sentence list to a custom list that uses the same format)
sentences = []
for s in sentences_raw:
	tokens = []
	for token in s:
		tokens.append({'id': token['id'], 'form': token['form'], 'tag': token['tag']})
	sentences.append(tokens)


def decode_sentence(sentence):
	word_list = []
	for word in sentence:
		word_list.append(word['form'])

		#sentence_decoded = baseline_decode(word_list)
		sentence_decoded = decode(word_list)

	csv_sentence = ""
	# Creating the csv for result comparison
	for index, token in enumerate(sentence):
		sd_token = sentence_decoded[index]
		is_correct = "yes" if token['tag'] == sd_token['tag'] else "no"
		csv_sentence += str(token['id']) + '\t' + token['form'] + '\t' + token['tag'] + '\t' + sd_token['tag'] + '\t' + is_correct + '\n'

	# End of sentence
	csv_sentence += '\n'
	return csv_sentence


# multi threading
csv_sentences = pqdm(sentences, decode_sentence, n_jobs=constants.NUM_CORES, desc="DECODING...")


# Write the result to a CSV
results_csv = 'ID\tWord\tTAG_Test\tTAG_Calculated\tIS_Correct\n'

for s in csv_sentences:
	results_csv += s

	#string_to_csv("BASELINE_results_comparison", results_csv)
	string_to_csv("results_comparison", results_csv)

