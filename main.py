from helpers import from_conllu_to_sentences, string_to_csv
import constants
from decode import decode
from pqdm.processes import pqdm


sentences_old = from_conllu_to_sentences(constants.IT_TEST_PATH)
results_csv = 'ID\tWord\tTAG_Test\tTAG_Calculated\tIS_Correct\n'

sentences = []

for s in sentences_old:
	tokens = []
	for t in s:
		tokens.append({'id': t['id'], 'form': t['form'], 'tag': t['tag']})
	sentences.append(tokens)


def decode_sentence(sentence):

	csv_sentence = ""
	word_list = []
	for w in sentence:
		word_list.append(w['form'])
	sentence_decoded = decode(word_list)

	# Creating the csv for result comparison
	for index, token in enumerate(sentence):
		sd_token = sentence_decoded[index]
		is_correct = "yes" if token['tag'] == sd_token['tag'] else "no"
		csv_sentence += str(token['id']) + '\t' + token['form'] + '\t' + token['tag'] + '\t' + sd_token['tag'] + '\t' + is_correct + '\n'

	# End of sentence
	csv_sentence += '\n'
	return csv_sentence


# multi threading
csv_sentences = pqdm(sentences, decode_sentence, n_jobs=constants.NUM_CORES)


for s in csv_sentences:
	results_csv += s

string_to_csv("results_comparison", results_csv)

