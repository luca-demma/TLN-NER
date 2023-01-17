from helpers import from_conllu_to_sentences, string_to_csv
import constants
from decode import decode
from tqdm import tqdm


sentences = from_conllu_to_sentences(constants.IT_TEST_PATH)
results_csv = 'ID\tWord\tTAG-Test\tTAG-Actual\n'

for s in tqdm(sentences):
	word_list = []
	for w in s:
		word_list.append(w['form'])
	sentence_decoded = decode(word_list)

	# Creating the csv for result comparison
	for index, token in enumerate(s):
		sd_token = sentence_decoded[index]
		results_csv += str(token['id']) + '\t' + token['form'] + '\t' + token['tag'] + '\t' + sd_token['tag'] + '\n'

	# End of sentence
	results_csv += '\n'

string_to_csv("results_comparison", results_csv)
