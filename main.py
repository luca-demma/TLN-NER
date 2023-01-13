from conllu import parse

DATA_PATH = "./data"
DATA_IT_DIR = "wikineural_it"
DATA_EN_DIR = "wikineural_en"

TRAIN_FILE = "train.conllu"
TEST_FILE = "test.conllu"
VAL_FILE = "val.conllu"

IT_TRAIN_PATH = DATA_PATH + "/" + DATA_IT_DIR + "/" + TRAIN_FILE
IT_TEST_PATH = DATA_PATH + "/" + DATA_IT_DIR + "/" + TEST_FILE
IT_VAL_PATH = DATA_PATH + "/" + DATA_IT_DIR + "/" + VAL_FILE

#TODO en paths

with open(IT_TRAIN_PATH) as f:
	train_text = f.read()
	sentences = parse(train_text, fields=["id", "form", "tag"])

sentence = sentences[0]
print(sentence)


