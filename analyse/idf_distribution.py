# -*- coding: utf-8 -*-
"""
@author: liluoqin
@function:
    1.idf分布
"""
import matplotlib.pyplot as plt


def print_freq_dis(value, label, save_pic, xlabel, ylabel, range_num):
    """
    print the frequency distribution in value
    :param value:
    :param label:
    :param save_pic: save path
    :param xlabel:
    :param ylabel:
    :return:
    """
    plt.figure(figsize=(8, 8))
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    n, bins, patches = plt.hist(value, range_num, align='mid', label=label, density=True)

    # 标注数字
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(save_pic)
    plt.show()
    return n, bins


if __name__ == "__main__":
    idf_value = []
    file_name = "./idf.txt"
    with open(file_name, "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if line:
                idf_value.append(float(line.split(" ")[1]))
            else:
                break

    idf_value.sort()
    save_pic = "../picture/idf-value.png"
    n, bins = print_freq_dis(idf_value, "idf", save_pic, "idf", "frequency", 100)