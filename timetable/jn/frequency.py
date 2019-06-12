import re
import os
import sys
import glob
import pandas as pd
import numpy as np
import datetime

from html.parser import HTMLParser
import sys
import re


class HTMLTableParser(HTMLParser):
    def __init__(self, row_delim="\n", cell_delim="\t"):
        HTMLParser.__init__(self)
        self.despace_re = re.compile(r'\s+')
        self.data_interrupt = False
        self.first_row = True
        self.first_cell = True
        self.in_cell = False
        self.row_delim = row_delim
        self.cell_delim = cell_delim

    def handle_starttag(self, tag, attrs):
        self.data_interrupt = True
        if tag == "table":
            self.first_row = True
            self.first_cell = True
        elif tag == "tr":
            if not self.first_row:
                sys.stdout.write(self.row_delim)
            self.first_row = False
            self.first_cell = True
            self.data_interrupt = False
        elif tag == "td" or tag == "th":
            if not self.first_cell:
                sys.stdout.write(self.cell_delim)
            self.first_cell = False
            self.data_interrupt = False
            self.in_cell = True

    def handle_endtag(self, tag):
        self.data_interrupt = True
        if tag == "td" or tag == "th":
            self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            # if self.data_interrupt:
            #   sys.stdout.write(" ")
            sys.stdout.write(self.despace_re.sub(' ', data).strip())
            self.data_interrupt = False


parser = HTMLTableParser()


def main():
    file_list = glob.glob(os.getcwd()+"/*.html")
    temp = []

    for each_one in file_list:
        htmlfile = parser
        data = pd.read_html(each_one, header=0)

        route_info = data[0].columns.values.tolist()[0]
        stop_name = re.compile('总站名称：\S+').findall(route_info)[0]
        stop_name_1 = re.compile('：\S+').findall(stop_name)
        stop_name_str = re.compile('\w+').findall(stop_name_1[0])[0]
        route_ID = re.compile('线路：\S+').findall(route_info)
        route_ID_num = re.compile('\w?\d+').findall(route_ID[0])[0]

        depart_time = data[0].iloc[:, 10]
        index = index = pd.DatetimeIndex(depart_time[11:])

        temp_data = pd.Series([a for a in range(len(index))], index=index)

        time_1 = datetime.datetime.today().strftime('%Y-%m-%d')+' 07:00:00'
        time_2 = datetime.datetime.today().strftime('%Y-%m-%d')+' 09:00:00'

        time_3 = datetime.datetime.today().strftime('%Y-%m-%d')+' 13:30:00'
        time_4 = datetime.datetime.today().strftime('%Y-%m-%d')+' 15:30:00'

        time_5 = datetime.datetime.today().strftime('%Y-%m-%d')+' 17:00:00'
        time_6 = datetime.datetime.today().strftime('%Y-%m-%d')+' 19:00:00'

        total_num = len(temp_data)
        num_1 = len(temp_data[time_1:time_2])
        num_2 = len(temp_data[time_3:time_4])
        num_3 = len(temp_data[time_5:time_6])

        temp.append([route_ID_num, stop_name_str,
                     total_num, num_1, num_2, num_3])

    table = pd.DataFrame(temp, columns=[
        'route_ID_num', 'stop_name_str', 'total_num', 'num_1', 'num_2', 'num_3'])

    table.to_csv('output.csv', encoding='utf_8_sig', index=False)


if __name__ == "__main__":
    main()
