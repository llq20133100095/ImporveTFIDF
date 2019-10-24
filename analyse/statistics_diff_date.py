# -*- coding: utf-8 -*-
"""
@author: liluoqin
@function:
    1.统计不同的日期的重合和不重合的涨跌情况
"""
import sys
sys.path.append("..")
from analyse.get_completion import read_file_name
import os
import re

spe_pattern = re.compile(".*?(,[0-9].)")


def cal_keywords_number(filename, filename_short, numbers_dict, date):
    """
    calculate the number of keywords in done.csv
    :param filename:
    :param filename_short:
    :param numbers_dict:
    :return:
    """
    file_len = len(open(filename, "r", encoding="utf-8").readlines())

    if file_len > 201:
        return
    else:
        keywords_num = 0
        with open(filename, "r", encoding="utf-8") as f:
            line = f.readline()
            while True:
                line = f.readline()
                if line:
                    spe_match = spe_pattern.match(line)
                    split_pos = line.index(spe_match.group(1))
                    word = line[:split_pos]
                    if not word.isdigit():
                        keywords_num += 1
                else:
                    break

        # save the keywords_num
        id_name = filename_short[:filename_short.index(filename_short.split("_")[2] + "_" + filename_short.split("_")[3]) - 1]
        if id_name not in numbers_dict.keys():
            numbers_dict[id_name] = [date + ":" + str(keywords_num)]
        else:
            numbers_dict[id_name].append(date + ":" + str(keywords_num))


def change_csv_to_dict(csv_file):
    """
    change csv to dict
    :param csv_file:
    :return: number_lpid_dict
    """
    number_lpid_dict = {}
    with open(csv_file, "r", encoding="utf-8") as f:
        line = f.readline()
        while True:
            line = f.readline()
            if line:
                line_list = line.strip("\n").split(",")
                key = line_list[2] + "_" + line_list[1]
                value = line_list[0] + ":" + line_list[5]
                if key not in number_lpid_dict.keys():
                    number_lpid_dict[key] = [value]
                else:
                    number_lpid_dict[key].append(value)
            else:
                break
    return number_lpid_dict


def look_up_same_file(keywords_number_dict, save_file, date_list):
    """
    generate txt file in different date
    :param keywords_number_dict:(keys:gameid_lpid, date:nums)
    :param save_file:
    :param date_list:
    :return:
    """
    for key_word in keywords_number_dict.keys():
        save_list = []
        key_word_list = key_word.split("_")
        gameid = key_word_list[0]
        lpid = key_word_list[1]

        save_list.append(gameid)
        save_list.append(lpid)

        date_num_dict = {}
        for elemonent in keywords_number_dict[key_word]:
            ele_list = elemonent.split(":")
            date_store = ele_list[0]
            keywords_num = ele_list[1]

            date_num_dict[date_store] = keywords_num

        for date in date_list:
            if date in date_num_dict.keys():
                save_list.append(date_num_dict[date])
            else:
                save_list.append("Null")

        save_file.write("\t".join(save_list) + "\n")


if __name__ == "__main__":
    dir_path = os.path.dirname(__file__)

    """
    1. tf-idf 
    """
    path = "/data/datacenter/zhangxiang2/top30_sliding_1/danmu/statistics_top100_keywords"
    date_list = ["2019-08-13",  "2019-08-14",  "2019-08-15"]
    platfrom = ["huya"]
    game_label = ["1", "2336", "2793", "3203"]
    keywords_number_dict = {}
    save_file = open(os.path.join(dir_path, "../data/date_compare/20190813_to_0815_compare.txt"), "w", encoding="utf-8")

    for date in date_list:
        for pl in platfrom:
            for game in game_label:
                filename_list = []
                file_name_short = []
                file_dir = os.path.join(path, date, pl, game)
                read_file_name(filename_list, file_name_short, file_dir)

                # get number of keyword_num
                for index, filename in enumerate(filename_list):
                    cal_keywords_number(filename, file_name_short[index], keywords_number_dict, date)

    # save data
    save_list_title = []
    save_list_title.append("gameid")
    save_list_title.append("lpid")
    for date in date_list:
        save_list_title.append(date)
    save_file.write("\t".join(save_list_title) + "\n")
    look_up_same_file(keywords_number_dict, save_file, date_list)
    save_file.close()


    """
    2. onTV rate
    """
    # csv_file = "E:/弹幕质量分析/弹幕关键词统计/lpid_compare/20190701_to_0728_onTV_rate.csv"
    # save_file = open(os.path.join(dir_path, "../data/date_compare/20190701_to_0728_compare_onTV_rate.txt"), "w", encoding="utf-8")
    # date_list = ["2019-07-01",  "2019-07-02",  "2019-07-07",  "2019-07-08",  "2019-07-09",  "2019-07-14",  "2019-07-15",  "2019-07-16",  "2019-07-21",  "2019-07-22",  "2019-07-23",  "2019-07-28"]
    #
    # save_list_title = []
    # save_list_title.append("gameid")
    # save_list_title.append("lpid")
    # for date in date_list:
    #     save_list_title.append(date)
    # save_file.write("\t".join(save_list_title) + "\n")
    #
    # number_onTV_rate_dict = change_csv_to_dict(csv_file)
    # look_up_same_file(number_onTV_rate_dict, save_file, date_list)
    # save_file.close()