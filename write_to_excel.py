import pandas as pd
import constants


def write_to_excel(dict_2d, file_name):
	df = pd.DataFrame(dict_2d)
	# df.to_csv(OUTPUT_PATH + 'ccc.csv', index=None)
	df.to_excel(constants.OUTPUT_PATH + file_name + '.xlsx', na_rep=0, columns=df.columns)
