# -*- coding: utf-8 -*-
"""
@author: liluoqin
@function:
    工具类
"""
import os


def mkdir(path):
    """
    if the path doesn't exist, make the dirs of its.
    :param path:
    :return:
    """
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def read_filename(filename_list, file_name_short, file_dir, flag):
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
            if flag in file:
                filename_list.append(os.path.join(root, file))
                file_name_short.append(file)

def swap(nums, i, j):
    """
    swap two value
    :param nums:
    :param i:
    :param j:
    :return:
    """
    temp = nums[i]
    nums[i] = nums[j]
    nums[j] = temp


def sort_list(bilibili_filename_list, bilibili_filename_short):
    """
    :param bilibili_filename_list:
    :param bilibili_filename_short:
    :return:
    """
    # get the id
    import re
    # number_com = re.compile('^([0-9]+)\s')
    number_com = re.compile('.*?([0-9]+)')

    number_id = []
    for file_name in bilibili_filename_short:
        # use pattern to recoginze number
        # matcher = number_com.match(file_name)
        # if (matcher):
        #     number_id.append(int(matcher.group(1)))
        number_id.append(int(file_name.split("_")[2]))

    # sort the list
    for file_index in range(len(number_id)):
        min_index = file_index;
        for file_index2 in range(file_index + 1, len(number_id)):
            if number_id[min_index] > number_id[file_index2]:
                min_index = file_index2

        swap(number_id, min_index, file_index)
        swap(bilibili_filename_list, min_index, file_index)
        swap(bilibili_filename_short, min_index, file_index)
    return number_id