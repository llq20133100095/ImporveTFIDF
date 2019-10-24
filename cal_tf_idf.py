# -*- coding: utf-8 -*-
"""
@author: liluoqin
@function:
    1.calculate the tf value and idf value.（同时针对b站的数据去掉了“undefined”词语）
    2.计算输出tf，idf的值
    3.计算不在jieba语料库中的idf词语
    4.统计top100的关键词数据
"""
import os
from analyse.tfidf import TFIDF
from analyse.get_completion import get_completion_main
import pandas as pd
import time
import re
import multiprocessing
from util.use_tool import sort_list

dir_path = os.path.dirname(__file__)
english_com = re.compile(".*?([a-zA-Z]+)")

def mkdir(path):
    """
    if the path doesn't exist, make the dirs of its.
    :param path:
    :return:
    """
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


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
            # if platform in file and game in file:
            # if "done2" not in file:
            if label in file:
                filename_list.append(os.path.join(root, file))
                file_name_short.append(file)



def read_content_cal_tf_idf(path, save_path, count, threshold):
    """
    get the 'danmu' contant.
    and calculate the tf-idf value
    :param path:
    :param save_path:
    :param count:
    :param threshold: 0.01
    :return:
    """
    data = []
    with open(path, encoding="utf-8") as f:
        re = f.readlines()
        for line in re:
            line = line.strip()
            english_match = english_com.match("Call")
            if (line != "NULL" and line != "msg" and line != 'undefined'):
                if english_match and len(english_match.group(1)) == len(line):
                    continue
                data.append(line + " ")

    stopwords = []
    file = open("stopwords.txt", encoding="utf-8")
    while True:
        line = file.readline()
        line = line.strip()
        stopwords.append(line)
        if not line:
            break
    stopwords.append(" ")
    stopwords.append("NULL")

    # analyse.set_stop_words("stopwords.txt")
    # use = analyse.extract_tags("".join(data), topK=count, withWeight=True, allowPOS=())
    # use the TFIDF
    default_tfidf = TFIDF()
    default_tfidf.set_stop_words("stopwords.txt")
    # get the tf-value and the total words numbers
    tf_freq, total, use = default_tfidf.extract_tags("".join(data), topK=count, withWeight=True, allowPOS=())

    # get idf_value
    idf_value = default_tfidf.idf_freq

    # save words, tf-idf, tf, idf
    words = []
    freqs = []
    tf = []
    idf = []
    words_num = []
    for line in use:
        if(threshold): # if the threshold has value
            # if(line[1] > threshold and not line[0].isdigit()):
            if (line[1] > threshold):
                words.append(line[0])
                freqs.append(line[1])
                # get the TF value
                tf.append(tf_freq[line[0]] / total)
                idf.append(idf_value.get(line[0], default_tfidf.median_idf))
                words_num.append(total)
        else:
            words.append(line[0])
            freqs.append(line[1])
            # get the TF value
            tf.append(tf_freq[line[0]] / total)
            idf.append(idf_value.get(line[0], default_tfidf.median_idf))
            words_num.append(total)

    ret = pd.DataFrame({'word': words, 'tf-idf': freqs, 'tf': tf, 'idf': idf, 'words_num': words_num})
    columns = ['word', 'tf-idf', 'tf', 'idf', 'words_num']
    ret.to_csv(save_path, header=True, index=None, encoding="utf-8-sig", columns=columns)

    # statistics the keywords_num
    keywords_num = 0
    for word in words:
        if(not word.isdigit()):
            keywords_num += 1

    return default_tfidf, use, keywords_num


def change_to_raw(file_dir):
    """
    change the "csv" to "_raw.csv"
    :param file_dir:
    :return:
    """
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_name = os.path.join(root, file)
            os.rename(file_name, file_name.replace(".csv", "_raw.csv"))


def cal_no_idf(path, count, threshold):
    """
    calculate the number of "all words" and the number of "no_idf_words"
    :param path:
    :param count:
    :param threshold:
    :return:
    """
    data = []
    with open(path, encoding="utf-8") as f:
        re = f.readlines()
        for line in re:
            line = line.strip()
            if (line != "NULL" and line != "msg" and line != 'undefined'):
                data.append(line + " ")

    stopwords = []
    file = open("stopwords.txt", encoding="utf-8")
    while True:
        line = file.readline()
        line = line.strip()
        stopwords.append(line)
        if not line:
            break
    stopwords.append(" ")
    stopwords.append("NULL")

    # use the TFIDF
    default_tfidf = TFIDF()
    default_tfidf.set_stop_words("stopwords.txt")
    # get the tf-value and the total words numbers
    tf_freq, total, use = default_tfidf.extract_tags("".join(data), topK=count, withWeight=True, allowPOS=())

    # get idf_value
    idf_value = default_tfidf.idf_freq

    # save words, no_idf_words
    words = []
    for line in use:
        if(threshold): # if the threshold has value
            if (line[1] > threshold):
                words.append(line[0])
                # if(line[0] not in idf_value.keys()):
                #     no_idf_words.append(line[0])
        else:
            words.append(line[0])
            # if (line[0] not in idf_value.keys()):
            #     no_idf_words.append(line[0])

    # if greater 200
    words_greater = 0.0
    words_less = 0.0
    no_idf_words_greater = 0.0
    no_idf_words_less = 0.0
    no_idf_words = []
    if(len(words) >= 200):
        words_greater = len(words)
        for w in words:
            if(w not in idf_value.keys()):
                no_idf_words.append(w)

        no_idf_words_greater = len(no_idf_words)
    else:
        words_less = len(words)
        for w in words:
            if(w not in idf_value.keys()):
                no_idf_words.append(w)

        no_idf_words_less = len(no_idf_words)

    return words_greater, words_less, no_idf_words_greater, no_idf_words_less


def cal_keywords(path, count, threshold, topN, filename_short, save_path, date, platform, game, dir_path):
    """
    calculate number of keywords in topN
    :param path:
    :param count: the parameter in tf-idf
    :param threshold: 0.01
    :param topN: 100 or 300
    :param filename_short: short name, no have the path
    :param save_path: save the data
    :return:
    """
    keywords_num = 0

    # #check if have the topN
    # import re
    # number_com = re.compile('^([0-9]+)\s')
    # # number_com = re.compile('.*?([0-9]+)')
    # matcher = number_com.match(filename_short)
    # if(matcher and int(matcher.group(1)) <= topN):

    data = []
    with open(path, encoding="utf-8") as f:
        re = f.readlines()
        for line in re:
            line = line.strip()
            if (line != "NULL" and line != "msg" and line != 'undefined'):
                data.append(line + " ")

    stopwords = []
    file = open("stopwords.txt", encoding="utf-8")
    while True:
        line = file.readline()
        line = line.strip()
        stopwords.append(line)
        if not line:
            break
    stopwords.append(" ")
    stopwords.append("NULL")

    # use the TFIDF
    default_tfidf = TFIDF()
    default_tfidf.set_stop_words("stopwords.txt")
    # get the tf-value and the total words numbers
    tf_freq, total, use = default_tfidf.extract_tags("".join(data), topK=count, withWeight=True, allowPOS=())

    # get idf_value
    idf_value = default_tfidf.idf_freq

    # save words, tf-idf, tf, idf
    words = []
    freqs = []
    tf = []
    idf = []
    words_num = []
    for line in use:
        if(threshold): # if the threshold has value
            # if(line[1] > threshold and not line[0].isdigit()):
            if (line[1] > threshold):
                words.append(line[0])
                freqs.append(line[1])
                # get the TF value
                tf.append(tf_freq[line[0]] / total)
                idf.append(idf_value.get(line[0], default_tfidf.median_idf))
                words_num.append(total)
        else:
            words.append(line[0])
            freqs.append(line[1])
            # get the TF value
            tf.append(tf_freq[line[0]] / total)
            idf.append(idf_value.get(line[0], default_tfidf.median_idf))
            words_num.append(total)

    fin_num = len(words)

    # save data
    mkdir(save_path)
    save_path = os.path.join(save_path, filename_short.replace(".csv", "_done.csv"))
    ret = pd.DataFrame({'word': words, 'tf-idf': freqs})
    columns = ['word', 'tf-idf']
    ret.to_csv(save_path, header=True, index=None, encoding="utf-8-sig", columns=columns)

    # statistics the keywords_num
    for word in words:
        if(not word.isdigit()):
            keywords_num += 1

    if(fin_num <= 200):
        topN -= 1
    else:
        keywords_num = 0

    return keywords_num, topN


def multiprocess_cal_keywords(count, threshold, topN, game, jobId, date, pf, save_path, dir_path):
    """
    multiple process: calculate the number of keywords in each date.
    :param count:
    :param threshold:
    :param topN:
    :param game:
    :param jobId:
    :param date:
    :param pf:
    :param save_path:
    :param dir_path:
    :return:
    """
    raw = "raw"  # or "raw_all"

    # concate the save path
    save_path = os.path.join(save_path, date, pf)

    print("start %s job in %s date_platform" % (jobId, date + "_" + pf))
    start_time = time.time()

    total_key_num = 0.0

    # calculate the number of file: if the keywords < 200, cal_topN -= 1
    cal_topN = topN

    # read all file
    bilibili_filename_list = []
    bilibili_filename_short = []

    # if in "raw"
    # read_file_name(bilibili_filename_list, bilibili_filename_short, os.path.join(path, game))
    read_file_name(bilibili_filename_list, bilibili_filename_short, os.path.join(dir_path, date, raw), pf, game)

    # sort the list
    sort_list(bilibili_filename_list, bilibili_filename_short)

    new_save_path = os.path.join(save_path, game)
    for index, filename in enumerate(bilibili_filename_list):
        if(cal_topN > 0):
            keywords_num, cal_topN = cal_keywords(filename, count, threshold, cal_topN, bilibili_filename_short[index], new_save_path, date, pf, game, dir_path)

            # calculate in bootstrap
            # _, _, keywords_num, cal_topN, _, _, _ = cal_tf_idf_in_bootstrap(
            #     filename, new_save_path, count, cal_topN, bilibili_filename_short[index])

            total_key_num += keywords_num

    # print the number of keywords
    print("job: %s and date_platform: %s and game_name: %s and keywords_num: %d" \
          % (jobId, date + "_" + pf, game, total_key_num))


if __name__ == "__main__":
    # bilibili_path = u'E:/弹幕质量分析/异常数据集'
    bilibili_path = u'/data/datacenter/zhangxiang2/top30_sliding_1/danmu'
    bilibili_filename_list = []
    bilibili_filename_short = []
    count = False
    threshold = 0.01

    # get the file name
    change_to_raw(bilibili_path) # no have the "raw.csv"
    read_file_name(bilibili_filename_list, bilibili_filename_short, bilibili_path, "1", "1")

    """1.print the tf-idf in all words. The threshold must have the value."""
    # read the csv and calculate the tf-idf
    total_key_num = 0.0
    for index, filename in enumerate(bilibili_filename_list):
        save_path = os.path.join(bilibili_path, bilibili_filename_short[index].replace(".csv", "_done2.csv"))
        default_tfidf, use, keywords_num = read_content_cal_tf_idf(filename, save_path, count, threshold)
        total_key_num += keywords_num
        # if(keywords_num > 200):
        print("finish %d-file" % (index + 1))
        print("file name %s and keywords_num %d" % (bilibili_filename_short[index], keywords_num))

    idf_value = default_tfidf.idf_freq
    median_idf = default_tfidf.median_idf
    print("median_idf: %f" % median_idf)
    print("keywords_num: %d" % total_key_num)