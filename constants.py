from enum import Enum
import sys
import multiprocessing

NUM_CORES = multiprocessing.cpu_count()

DATA_PATH = "./data"
DATA_IT_DIR = DATA_PATH + "/wikineural_it/"
DATA_EN_DIR = DATA_PATH + "/wikineural_en/"

TRAIN_FILE = "train.conllu"
TEST_FILE = "test.conllu"
VAL_FILE = "val.conllu"

IT_TRAIN_PATH = DATA_IT_DIR + TRAIN_FILE
IT_TEST_PATH = DATA_IT_DIR + TEST_FILE
IT_VAL_PATH = DATA_IT_DIR + VAL_FILE

MIN_FLOAT = -sys.float_info.max

OUTPUT_PATH = DATA_PATH + "/outputs/"

#TODO english paths


class NerTag(Enum):
#	START = "START"
	B_PER = "B-PER"
	I_PER = "I-PER"
	B_ORG = "B-ORG"
	I_ORG = "I-ORG"
	B_LOC = "B-LOC"
	I_LOC = "I-LOC"
	B_MISC = "B-MISC"
	I_MISC = "I-MISC"
	OTHER = "O"
