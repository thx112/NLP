#!/usr/bin/env python3
# coding: utf-8
# File: jieba_TF-IDF.py
# Author: thx112
# Desc: 基于 TF-IDF（term frequency–inverse document frequency） 算法的关键词抽取

import jieba.analyse as aly

content = '''
自然语言处理（NLP）是计算机科学，人工智能，语言学关注计算机和人类（自然）语言之间的相互作用的领域。
因此，自然语言处理是与人机交互的领域有关的。在自然语言处理面临很多挑战，包括自然语言理解，因此，自然语言处理涉及人机交互的面积。
在NLP诸多挑战涉及自然语言理解，即计算机源于人为或自然语言输入的意思，和其他涉及到自然语言生成。
'''

#加载自定义idf词典
aly.set_idf_path('../data/idf.txt.big')
#加载停用词典
aly.set_stop_words('../data/stop_words.utf8')

# 第一个参数：待提取关键词的文本
# 第二个参数：返回关键词的数量，重要性从高到低排序
# 第三个参数：是否同时返回每个关键词的权重
# 第四个参数：词性过滤，为空表示不过滤，若提供则仅返回符合词性要求的关键词
keywords = aly.extract_tags(content, topK=10, withWeight=True, allowPOS=())

for item in keywords:
    # 分别为关键词和相应的权重
    print(item[0], item[1])
    
    
# output
# 自然语言 2.0790900005043476
# NLP 0.5197725001260869
# 计算机 0.5197725001260869
# 领域 0.5197725001260869
# 人机交互 0.5197725001260869
# 挑战 0.5197725001260869
# 理解 0.5197725001260869
# 处理 0.4705091875965217
# 涉及 0.3839134341652174
# 人工智能 0.25988625006304344