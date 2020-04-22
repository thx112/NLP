#!/usr/bin/env python3
# coding: utf-8
# open: participle_hmm.py
# Author: thx112
# Desc: Using hmm to achieve participle

import os
import pickle

class HMM(object):
    def __init__(self):
        self.model_file = './data/hmm_model.pkl' # 主要是用于存取算法中间结果，不用每次都训练模型
        self.state_list = ['B', 'M', 'E', 'S']  # 状态值集合
        self.load_para = False # 参数加载,用于判断是否需要重新加载model_file

    # 用于加载已计算的中间结果，当需要重新训练时，需初始化清空结果
    def try_load_model(self, trained):
        if trained:
            with open(self.model_file, 'rb') as f:
                self.A_dict = pickle.load(f)
                self.B_dict = pickle.load(f)
                self.Pi_dict = pickle.load(f)
                self.load_para = True
        else:
            self.A_dict = {}  # 状态转移概率（状态->状态的条件概率）
            self.B_dict = {}  # 发射概率（状态->词语的条件概率）
            self.Pi_dict = {} # 状态的初始概率
            self.load_para = False

    # 计算转移概率、发射概率以及初始概率
    def train(self, path):
        self.try_load_model(False)  # 重置几个概率矩阵
        count_dict = {}  # 统计状态出现次数，求p(o)

        # 初始化参数
        def init_parameters():
            for state in self.state_list:
                self.A_dict[state] = {s: 0.0 for s in self.state_list}
                self.Pi_dict[state] = 0.0
                self.B_dict[state] = {}
                count_dict[state] = 0
        def make_label(text):
            '''
            S:单字词
            B:词的开头
            M:词的中间
            E:词的末尾
            好 ['S']
            去哪 ['B', 'E']
            你去哪 ['B', 'M', 'E']
            '''
            out_text = []
            if len(text) == 1:
                out_text.append('S')
            else:
                out_text += ['B'] + ['M'] * (len(text) - 2) + ['E']
            return out_text

        init_parameters()
        line_num = -1
        
        words = set() # 观察者集合，主要是字以及标点等
        with open(path, encoding='utf8') as f:
            for line in f:
                line_num += 1
                line = line.strip()
                if not line:
                    continue

                word_list = [i for i in line if i != ' ']
                words |= set(word_list)  # 更新字的集合
                line_list = line.split()

                line_state = []
                for w in line_list:
                    line_state.extend(make_label(w))
                
                assert len(word_list) == len(line_state)

                for k, v in enumerate(line_state):
                    count_dict[v] += 1
                    if k == 0:
                        self.Pi_dict[v] += 1  # 每个句子的第一个字的状态，用于计算初始状态概率
                    else:
                        self.A_dict[line_state[k - 1]][v] += 1  # 计算转移概率
                        self.B_dict[line_state[k]][word_list[k]] = \
                            self.B_dict[line_state[k]].get(word_list[k], 0) + 1.0  # 计算发射概率
        
        self.Pi_dict = {k: v * 1.0 / line_num for k, v in self.Pi_dict.items()}
        self.A_dict = {k: {k1: v1 / count_dict[k] for k1, v1 in v.items()}
                      for k, v in self.A_dict.items()}
        #加1平滑
        self.B_dict = {k: {k1: (v1 + 1) / count_dict[k] for k1, v1 in v.items()}
                      for k, v in self.B_dict.items()}
        #序列化
        with open(self.model_file, 'wb') as f:
            pickle.dump(self.A_dict, f)
            pickle.dump(self.B_dict, f)
            pickle.dump(self.Pi_dict, f)

        return self

    def viterbi(self, text, states, start_p, trans_p, emit_p):
        V = [{}]
        path = {}
        for y in states:
            V[0][y] = start_p[y] * emit_p[y].get(text[0], 0)
            path[y] = [y]
        for t in range(1, len(text)):
            V.append({})
            newpath = {}
            
            #检验训练的发射概率矩阵中是否有该字
            neverSeen = text[t] not in emit_p['S'].keys() and \
                text[t] not in emit_p['M'].keys() and \
                text[t] not in emit_p['E'].keys() and \
                text[t] not in emit_p['B'].keys()
            for y in states:
                emitP = emit_p[y].get(text[t], 0) if not neverSeen else 1.0 #设置未知字单独成词
                (prob, state) = max(
                    [(V[t - 1][y0] * trans_p[y0].get(y, 0) *
                      emitP, y0)
                     for y0 in states if V[t - 1][y0] > 0])
                V[t][y] = prob
                newpath[y] = path[state] + [y]
            path = newpath
            
        if emit_p['M'].get(text[-1], 0)> emit_p['S'].get(text[-1], 0):
            (prob, state) = max([(V[len(text) - 1][y], y) for y in ('E','M')])
        else:
            (prob, state) = max([(V[len(text) - 1][y], y) for y in states])
        
        return (prob, path[state])

    def cut(self, text):
        if not self.load_para:
            self.try_load_model(os.path.exists(self.model_file))
        prob, pos_list = self.viterbi(text, self.state_list, self.Pi_dict, self.A_dict, self.B_dict)      
        begin, next = 0, 0    
        for i, char in enumerate(text):
            pos = pos_list[i]
            if pos == 'B':
                begin = i
            elif pos == 'E':
                yield text[begin: i+1]
                next = i+1
            elif pos == 'S':
                yield char
                next = i+1
        if next < len(text):
            yield text[next:]


hmm = HMM()
#hmm.train('./data/trainCorpus.txt_utf8')

text = '今天下午打球时遇到一个很有趣的人!'
res = hmm.cut(text)
print(text)
print(str(list(res)))






    

