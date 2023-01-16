from conllu import parse
from enum import Enum
from collections import defaultdict
import json
import pandas as pd

DATA_PATH = "./data"
DATA_IT_DIR = "wikineural_it"
DATA_EN_DIR = "wikineural_en"

TRAIN_FILE = "train.conllu"
TEST_FILE = "test.conllu"
VAL_FILE = "val.conllu"

IT_TRAIN_PATH = DATA_PATH + "/" + DATA_IT_DIR + "/" + TRAIN_FILE
IT_TEST_PATH = DATA_PATH + "/" + DATA_IT_DIR + "/" + TEST_FILE
IT_VAL_PATH = DATA_PATH + "/" + DATA_IT_DIR + "/" + VAL_FILE

OUTPUT_PATH = DATA_PATH + "/outputs/"

#TODO en paths

with open(IT_TRAIN_PATH) as f:
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

# Print to EXCEL
df = pd.DataFrame(emissions_counts)
#df.to_csv(OUTPUT_PATH + 'ccc.csv', index=None)
df.to_excel(OUTPUT_PATH + 'emissions_count.xlsx', na_rep=0, columns=df.columns)


emissions_probabilities = multi_dict(2, float)

for t in emissions_counts.keys():
	for w in emissions_counts[t].keys():
		w_count = 0
		for tt in emissions_counts.keys():
			w_count += int(emissions_counts[tt][w])
		emissions_probabilities[t][w] = emissions_counts[t][w] / w_count

# Print to EXCEL
df = pd.DataFrame(emissions_probabilities)
#df.to_csv(OUTPUT_PATH + 'ccc.csv', index=None)
df.to_excel(OUTPUT_PATH + 'emissions_probabilities.xlsx', na_rep=0, columns=df.columns)


# [tag][prev_tag]
transitions_counts = multi_dict(2, int)

for s in sentences:
	for t in s:
		prev_tag = "START" if t['id'] == 0 else s[t['id'] - 1]['tag']
		transitions_counts[t['tag']][prev_tag] += 1

# Print to EXCEL
df = pd.DataFrame(transitions_counts)
#df.to_csv(OUTPUT_PATH + 'ccc.csv', index=None)
df.to_excel(OUTPUT_PATH + 'transitions_counts.xlsx', na_rep=0, columns=df.columns)
