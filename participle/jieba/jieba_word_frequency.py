#!/usr/bin/env python3
# coding: utf-8
# File: jieba_word_frequency.py
# Author: thx112
# Desc: 动态修改词频

import jieba
sent = '好丑的证件照片'
print('/ '.join(jieba.cut(sent, HMM=False)))

#jieba.suggest_freq(('证件','照片'), True)
jieba.suggest_freq(('证件照片'), True)
print('/ '.join(jieba.cut(sent, HMM=False)))


# output
# 好丑/ 的/ 证件/ 照片
# 好丑/ 的/ 证件照片