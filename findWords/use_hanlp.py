# -*- coding: utf-8 -*-
"""
@author: liluoqin
@function:
    1. find new words
"""
from pyhanlp import *
from util.use_tool import read_filename

if __name__ == "__main__":
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, "../大数据和小数据集的对比/")
    filename_list = []
    filename_short_list = []
    read_filename(filename_list, filename_short_list, file_path, "raw")

    # find new words
    text_str = []
    for index, file in enumerate(filename_list):
        with open(file, "r", encoding="utf-8") as f:
            f.readline()
            while True:
                line = f.readline()
                if line:
                    line = line.strip()
                    text_str.append(line)
                else:
                    break

    ret = HanLP.extractWords(" ".join(text_str), 100000, newWordsOnly=True)
    print(ret)
