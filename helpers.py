import pandas as pd
import constants
from collections import defaultdict

def write_to_file(dict_2d, file_name):
	df = pd.DataFrame(dict_2d)
	# df.to_csv(OUTPUT_PATH + 'ccc.csv', index=None)
	#df.to_excel(constants.OUTPUT_PATH + file_name + '.xlsx', na_rep=0, columns=df.columns)
	df.to_csv(constants.OUTPUT_PATH + file_name + '.csv')


# Utility function to create dictionary
def multi_dict(K, type):
	if K == 1:
		return defaultdict(type)
	else:
		return defaultdict(lambda: multi_dict(K-1, type))
