#!/usr/bin/env python3
# coding: utf-8
# File: jieba_cut.py
# Author: thx112
# Desc: jieba的四种分词模式


import jieba

sent = '自然语言处理是人工智能和语言学领域的分支学科。'
seg_list = jieba.cut(sent, cut_all=True)
print('全模式：', '/ ' .join(seg_list)) 
seg_list = jieba.cut(sent, cut_all=False)
print('精确模式：', '/ '.join(seg_list)) 
seg_list = jieba.cut(sent)  
print('默认精确模式：', '/ '.join(seg_list))
seg_list = jieba.cut_for_search(sent)  
print('搜索引擎模式', '/ '.join(seg_list))

# output
# 全模式： 自然/ 自然语言/ 语言/ 处理/ 是/ 人工/ 人工智能/ 智能/ 和/ 语言/ 语言学/ 领域/ 的/ 分支/ 学科/ / 
# 精确模式： 自然语言/ 处理/ 是/ 人工智能/ 和/ 语言学/ 领域/ 的/ 分支/ 学科/ 。
# 默认精确模式： 自然语言/ 处理/ 是/ 人工智能/ 和/ 语言学/ 领域/ 的/ 分支/ 学科/ 。
# 搜索引擎模式 自然/ 语言/ 自然语言/ 处理/ 是/ 人工/ 智能/ 人工智能/ 和/ 语言/ 语言学/ 领域/ 的/ 分支/ 学科/ 。