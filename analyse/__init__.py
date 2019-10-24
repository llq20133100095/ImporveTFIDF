# -*- coding: utf-8 -*-
from __future__ import absolute_import
from analyse.tfidf import TFIDF
try:
    from .analyzer import ChineseAnalyzer
except ImportError:
    pass

default_tfidf = TFIDF()

extract_tags = tfidf = default_tfidf.extract_tags
set_idf_path = default_tfidf.set_idf_path

def set_stop_words(stop_words_path):
    default_tfidf.set_stop_words(stop_words_path)