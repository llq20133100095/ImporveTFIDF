# -*- coding: utf-8 -*-
"""
@author: liluoqin
@function:
    1.计算大于1w条以下的数据量
"""
import os
import pandas as pd
import datetime


def read_file_name(filename_list, file_name_short, file_dir, label):
    """
    Get the all file name
    :param filename_list:
    :param file_name_short:
    :param file_dir:
    :param qq_flag: if have the "raw"
    :return:
    """
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if label in file:
                filename_list.append(os.path.join(root, file))
                file_name_short.append(file)


def top_N_nums(filename_list, file_name_short, topN, save_topN, save_sliding, save_file_name, save_less_1w, save_min_nums, save_max_nums):
    for index, file_name in enumerate(filename_list):
        each_data = pd.read_csv(file_name, encoding="utf-8")
        topN_data = each_data[each_data["rank"] <= topN]
        less_nums = len(topN_data[topN_data["scon_num"] < 10000])
        min_nums = topN_data["scon_num"].min()
        max_nums = topN_data["scon_num"].max()
        print("topN: %d | file_name: %s | less_nums: %d | min_nums: %d | max_nums: %d" % (topN, file_name_short[index], less_nums, min_nums, max_nums))

        year = file_name_short[index].split("_")[0][0:4]
        date1 = file_name_short[index].split("_")[0][4:]
        date2 = file_name_short[index].split("_")[1]
        date1 = datetime.datetime.strptime(year + date1, '%Y%m%d')
        date2 = datetime.datetime.strptime(year + date2, '%Y%m%d')
        delta = date2 - date1

        save_topN.append(topN)
        save_sliding.append(delta.days + 1)
        save_file_name.append(file_name_short[index])
        save_less_1w.append(less_nums)
        save_min_nums.append(min_nums)
        save_max_nums.append(max_nums)


def top_N_nums_in_date(date, data_each_date, topN, save_topN, save_date_list, save_less_1w, save_min_nums, save_max_nums, save_sub_topN, save_sub_less_nums):
    """
    cal the number of less 1w
    :param date:
    :param data_each_date:
    :param topN:
    :param save_topN:
    :param save_date_list:
    :param save_less_1w:
    :param save_min_nums:
    :param save_max_nums:
    :return:
    """
    topN_data = data_each_date[data_each_date["rank"] <= topN]
    less_nums = len(topN_data[topN_data["scon_num"] < 10000])
    min_nums = topN_data["scon_num"].min()
    max_nums = topN_data["scon_num"].max()

    # topN - 10 to topN
    sub_topN_data = data_each_date[data_each_date["rank"] <= topN]
    sub_topN_data = sub_topN_data[sub_topN_data["rank"] >= topN - 10]
    sub_less_nums = len(sub_topN_data[sub_topN_data["scon_num"] < 10000])

    save_topN.append(topN)
    save_date_list.append(date)
    save_less_1w.append(less_nums)
    save_min_nums.append(min_nums)
    save_max_nums.append(max_nums)
    save_sub_topN.append(str(topN - 10) + "_" + str(topN))
    save_sub_less_nums.append(sub_less_nums)


def split_each_date(filename_list, topN):
    """
    split the each date in "csv"
    :param filename_list:
    :param file_name_short:
    :return:
    """
    for index, file_name in enumerate(filename_list):
        each_data = pd.read_csv(file_name, encoding="utf-8")

        date_list = list(each_data.groupby("dt")["dt"].count().index)

        for date in date_list:
            # return each_data[each_data["dt"] == date]
            top_N_nums_in_date(date, each_data[each_data["dt"] == date], topN, save_topN, save_date_list, save_less_1w, save_min_nums, save_max_nums, save_sub_topN, save_sub_less_nums)


if __name__ == "__main__":
    path = "E:/弹幕质量分析/弹幕数/针对1天的弹幕数"
    filename_list = []
    file_name_short = []
    label = "移动端"
    read_file_name(filename_list, file_name_short, path, label)
    topN = 100

    """
    1. cal multiple files
    """
    # # top N
    # save_topN = []
    # save_file_name = []
    # save_less_1w = []
    # save_min_nums = []
    # save_max_nums = []
    # save_sliding = []
    # for i in range(10, topN + 10, 10):
    #     top_N_nums(filename_list, file_name_short, i, save_topN, save_sliding, save_file_name, save_less_1w, save_min_nums, save_max_nums)
    #
    # ret = pd.DataFrame({'topN': save_topN, 'sliding': save_sliding, 'file_name': save_file_name, 'less_1w': save_less_1w, 'min_nums': save_min_nums, 'max_nums': save_max_nums})
    # columns = ['topN', 'sliding', 'file_name', 'less_1w', 'min_nums', 'max_nums']
    # save_path = os.path.join(path, "topN中少于1w的数量.csv")
    # ret.to_csv(save_path, header=True, index=None, encoding="utf-8-sig", columns=columns)

    """ 
    2. statistics in each day
    """
    save_topN = []
    save_date_list = []
    save_less_1w = []
    save_min_nums = []
    save_max_nums = []
    save_sub_topN = []
    save_sub_less_nums = []
    for i in range(10, topN + 10, 10):
        split_each_date(filename_list, i)

    ret = pd.DataFrame({'topN': save_topN, 'date': save_date_list, 'less_1w': save_less_1w, 'min_nums': save_min_nums, 'max_nums': save_max_nums, 'sub_topN': save_sub_topN, 'sub_less_nums': save_sub_less_nums})
    columns = ['topN', 'date', 'less_1w', 'min_nums', 'max_nums', 'sub_topN', 'sub_less_nums']
    save_path = os.path.join(path, "topN中少于1w的数量.csv")
    ret.to_csv(save_path, header=True, index=None, encoding="utf-8-sig", columns=columns)
