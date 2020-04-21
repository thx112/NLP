#!/usr/bin/env python3
# coding: utf-8
# File: jieba_custom_thesaurus.py
# Author: thx112
# Desc: 自定应词典

import jieba 
#加载系统词典
jieba.set_dictionary('../data/dict.txt.big')

print('自定义词典内容：')
with open('../data/user_dict.utf8', 'r',encoding='utf-8') as f:
    for l in f:
        print(l)

print('------华丽的分割线-------')
sent = 'jieba分词非常好用，可以自定义金融词典！'
seg_list = jieba.cut(sent)
print('加载词典前:', '/ '.join(seg_list))

jieba.load_userdict('../data/user_dict.utf8')
seg_list = jieba.cut(sent)
print('加载词典后:', '/ '.join(seg_list))

# output
# 自定义词典内容：
# 大波浪 10
# jieba分词 n
# 金融词典 7
# ------华丽的分割线-------
# 加载词典前: jieba/ 分词/ 非常/ 好用/ ，/ 可以/ 自定义/ 金融/ 词典/ ！
# 加载词典后: jieba分词/ 非常/ 好用/ ，/ 可以/ 自定义/ 金融词典/ ！
