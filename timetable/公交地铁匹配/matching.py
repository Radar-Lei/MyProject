import pandas as pd
import numpy as np
import glob
import os
import sys
import re

def main():
	file_list = glob.glob(os.getcwd()+"/*.csv")
	temp = []
	for each_one in file_list:
	    
	    df = pd.read_csv(each_one,engine='python',encoding='UTF8')
	    
	    route_ID = re.compile('\d+').findall(each_one)[0]
	    
	    df.drop_duplicates('STATIONID',inplace=True)
	    
	    temp.append([route_ID]+list(np.array(df['STATIONID'])))
	    
	table = pd.DataFrame(temp)

	table.to_csv('output.csv', encoding='utf_8_sig', index=False, header=None)


if __name__ == "__main__":
    main()