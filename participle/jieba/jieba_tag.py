#!/usr/bin/env python3
# coding: utf-8
# File: jieba_tag.py
# Author: thx112
# Desc: 利用jieba进行中文词性标注

import jieba.posseg as psg

sent = '自然语言处理是人工智能和语言学领域的分支学科。'

seg_list = psg.cut(sent)

print(' '.join(['{0}/{1}'.format(w, t) for w, t in seg_list]))

# output
# 自然语言/l 处理/v 是/v 人工智能/n 和/c 语言学/n 领域/n 的/uj 分支/n 学科/n 。/x