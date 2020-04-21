#!/usr/bin/env python3
# coding: utf-8
# File: jieba_TextRank.py
# Author: thx112
# Desc: 基于 TextRank 算法的关键词抽取


import jieba.analyse as aly

content = '''
自然语言处理（NLP）是计算机科学，人工智能，语言学关注计算机和人类（自然）语言之间的相互作用的领域。
因此，自然语言处理是与人机交互的领域有关的。在自然语言处理面临很多挑战，包括自然语言理解，因此，自然语言处理涉及人机交互的面积。
在NLP诸多挑战涉及自然语言理解，即计算机源于人为或自然语言输入的意思，和其他涉及到自然语言生成。
'''
# 第一个参数：待提取关键词的文本
# 第二个参数：返回关键词的数量，重要性从高到低排序
# 第三个参数：是否同时返回每个关键词的权重
# 第四个参数：词性过滤，为空表示过滤所有，与TF—IDF不一样！
keywords = jieba.analyse.textrank(content, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
for item in keywords:
    # 分别为关键词和相应的权重
    print(item[0], item[1])