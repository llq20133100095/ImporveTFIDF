# -*- coding: utf-8 -*-
"""
@author: liluoqin
@function:
    1. evaluation with slop method
"""
import os
from util.use_tool import read_filename
from cal_tf_idf import read_content_cal_tf_idf


def normalization(input):
    max_v = max(input)
    min_v = min(input)
    for i in range(len(input)):
        input[i] = (input[i] - min_v) / (max_v - min_v)
    return input


def cal_slope(filename):
    ret = 0
    pre = 0
    no_start_cal = True
    with open(filename, "r", encoding="utf-8") as f:
        line = f.readline()
        while True:
            line = f.readline().strip()
            if line:
                line_list = line.split(",")
                cur = float(line_list[1])
                if no_start_cal:
                    no_start_cal = False
                else:
                    ret += pre - cur
                pre = cur
            else:
                break
    return ret


def cal_slope_in_tf(filename):
    ret = 0
    pre = 0
    no_start_cal = True
    tf = []
    with open(filename, "r", encoding="utf-8") as f:
        line = f.readline()
        while True:
            line = f.readline().strip()
            if line:
                line_list = line.split(",")
                tf.append(float(line_list[2]))
            else:
                break

    tf = sorted(tf, reverse=True)
    for value in tf:
        if no_start_cal:
            no_start_cal = False
        else:
            ret += pre - value
        pre = value

    return ret


def cal_slope_in_normalization(filename, topN=50):
    """
    calculate value of slope with normalization
    :param filename:
    :param topN:
    :return:
    """
    ret = 0
    pre = 0
    no_start_cal = True
    tf_idf = []
    with open(filename, "r", encoding="utf-8") as f:
        line = f.readline()
        while True:
            line = f.readline().strip()
            if line:
                line_list = line.split(",")
                tf_idf.append(float(line_list[1]))
            else:
                break

    tf_idf = normalization(tf_idf)
    line_index = 0
    for value in tf_idf:
        line_index += 1
        if line_index >= topN:
            if no_start_cal:
                no_start_cal = False
            else:
                ret += pre - value
            pre = value

    return ret


if __name__ == "__main__":
    dir_path = os.path.dirname(__file__)
    data_dir = os.path.join(dir_path, "../大数据和小数据集的对比")

    """ 1. generate tf-idf words """
    # # get filename
    # filename_list = []
    # file_name_short = []
    # flag = "raw"
    # read_filename(filename_list, file_name_short, data_dir, flag)
    #
    # # cal tf-idf
    # count = False
    # threshold = 0
    # for index, filename in enumerate(filename_list):
    #     default_tfidf, use, keywords_num = read_content_cal_tf_idf(filename, os.path.join(data_dir, file_name_short[index].replace("_raw", "_done")), count, threshold)
    #     print("file name %s and keywords_num %d" % (file_name_short[index], keywords_num))

    """ 2. cal slope """
    filename_list = []
    file_name_short = []
    flag = "done"
    read_filename(filename_list, file_name_short, data_dir, flag)

    for index, filename in enumerate(filename_list):
        ret = cal_slope_in_tf(filename)
        print("filename: %s | ret: %f" % (file_name_short[index], ret))
