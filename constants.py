from enum import Enum
import sys
import multiprocessing

NUM_CORES = multiprocessing.cpu_count()

DATA_PATH = "./data"
DATA_IT_DIR = DATA_PATH + "/wikineural_it/"
DATA_EN_DIR = DATA_PATH + "/wikineural_en/"

TRAIN_FILE = "train.conllu"
TEST_FILE = "test.conllu"
# VAL_FILE = "val.conllu"

IT_TRAIN_PATH = DATA_IT_DIR + TRAIN_FILE
IT_TEST_PATH = DATA_IT_DIR + TEST_FILE
# IT_VAL_PATH = DATA_IT_DIR + VAL_FILE

MIN_FLOAT = -sys.float_info.max

OUTPUT_PATH = DATA_PATH + "/outputs/"

#TODO english paths


NER_TAGS = ["B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-MISC", "I-MISC", "O"]
