# -*- coding: utf-8 -*-
"""
@author: liluoqin
@function:
    1.拿到补全的文件名，即是小于200的文件名
"""
import os
import re
from util.use_tool import sort_list


number_com = re.compile('.*?([0-9]+)')
dir_path = os.path.dirname(__file__)


def read_file_name(filename_list, file_name_short, file_dir):
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
            filename_list.append(os.path.join(root, file))
            file_name_short.append(file)


def mkdir(path):
    """
    if the path doesn't exist, make the dirs of its.
    :param path:
    :return:
    """
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def judge_is_completion(filename_list, file_name_short, completion_file_list, platform, game):
    """
    Is the file is completion file?
    """
    for index, filename in enumerate(filename_list):
        lines_len = len(open(filename, "r", encoding="utf-8").readlines())

        id = number_com.match(file_name_short[index]).group(1)
        pos = file_name_short[index].index(id) + len(id) + 1
        owner = file_name_short[index][pos:].replace("_done.csv", "")
        new_filename = os.path.join(platform + "_" + game + "_" + number_com.match(file_name_short[index]).group(1) + "_" + owner + ".csv")
        # if lines_len > 201 and index < 100:
        #     del_file_list.append(new_filename)
        # elif lines_len <= 201 and index >= 100:
        #     completion_file_list.append(new_filename)
        if lines_len <= 201:
            completion_file_list.append(new_filename)


def get_completion_main(statistics_path, platfrom, date_list, game_name, game_name_bilibili, save_file_name):
    for date in date_list:
        completion_file_list = []

        for pl in platfrom:
            if pl == "bilibili":
                game_name_list = game_name_bilibili

            else:
                game_name_list = game_name

            for game in game_name_list:
                filename_list = []
                file_name_short = []
                new_path = os.path.join(statistics_path, date, pl, game)
                read_file_name(filename_list, file_name_short, new_path)

                # sort the filename
                sort_list(filename_list, file_name_short)

                judge_is_completion(filename_list, file_name_short, completion_file_list, pl, game)

        if len(completion_file_list) != 0:
            completion_file_save = save_file_name + date + "_file_name.txt"

            with open(completion_file_save, "w", encoding="utf-8") as f:
                for line in completion_file_list:
                    f.write(line + "\n")


if __name__ == "__main__":
    save_path = "/data/datacenter/zhangxiang2/top20/danmu"
    statistics_path = os.path.join(save_path, "statistics_top100_keywords")
    # date_list = ["20190415", "20190429", "20190506", "20190513", "20190520", "20190527", "20190603", "20190610", "20190617", "20190624"]
    # date_list += ["20190701", "20190708", "20190715"]
    date_list = ['2019-07-01', '2019-07-02', '2019-07-07', '2019-07-08', '2019-07-09', '2019-07-14']
    date_list += ['2019-07-15', '2019-07-16', '2019-07-21', '2019-07-22', '2019-07-23', '2019-07-28']
    # platfrom = ["douyu", "huya", "bilibili"]
    platfrom = ["huya"]
    # game_name = ["刺激战场", "王者荣耀", "绝地求生", "英雄联盟", "和平精英"]
    game_name = ["1", "2336", "2793", "3203"]
    game_name_bilibili = ["手游#·#和平精英", "手游#·#王者荣耀", "网游#·#绝地求生", "网游#·#英雄联盟"]

    # save file name
    save_file_path = os.path.join(dir_path, "../data/all_file_name/top20_2/")
    mkdir(save_file_path)
    save_file_name = save_file_path + "39_top20_"

    del_file_list = []

    get_completion_main(statistics_path, platfrom, date_list, game_name, game_name_bilibili, save_file_name)





