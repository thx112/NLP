#!/usr/bin/env python3
# coding: utf-8
# File: maximum_match.py
# Author: thx112
# Desc: 分词的 最大前向匹配、最大后向匹配、双向最大前向匹配

class MaxMatch:
    def __init__(self,dict_path):
        self.dictionary = set()
        self.maximum = 0
        #读取词典
        with open(dict_path, 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.dictionary.add(line)
                if len(line) > self.maximum:
                    self.maximum = len(line)
    #最大向前匹配
    def max_forward_cut(self, text):
        #1.从左向右取待切分汉语句的m个字符作为匹配字段，m为大机器词典中最长词条个数。
        #2.查找大机器词典并进行匹配。若匹配成功，则将这个匹配字段作为一个词切分出来。
        cutlist = []
        index = 0
        while index < len(text):
            matched = False
            for i in range(self.maximum, 0, -1):
                cand_word = text[index : index + i]
                if cand_word in self.dictionary:
                    cutlist.append(cand_word)
                    matched = True
                    break
            #如果没有匹配上，则按字符切分
            if not matched:
                i = 1
                cutlist.append(text[index])
            index += i
        return cutlist
    
    #最大后向匹配
    def max_backward_cut(self, text):
        #1.从右向左取待切分汉语句的m个字符作为匹配字段，m为大机器词典中最长词条个数。
        #2.查找大机器词典并进行匹配。若匹配成功，则将这个匹配字段作为一个词切分出来。
        cutlist = []
        index = len(text)
        while index > 0 :
            matched = False
            for i in range(self.maximum, 0, -1):
                if index - i < 0:  
                    continue
                cand_word = text[index - i : index]
                #如果匹配上，则将字典中的字符加入到切分字符中
                if cand_word in self.dictionary:
                    cutlist.append(cand_word)
                    matched = True
                    index -= i
                    break
            #如果没有匹配上，则按字符切分
            if not matched:
                index -= 1
                cutlist.append(text[index-1])
        return cutlist[::-1]  

    # 双向最大前向匹配
    def max_biward_cut(self, text):
        # 双向最大匹配法是将正向最大匹配法得到的分词结果和逆向最大匹配法的到的结果进行比较，从而决定正确的分词方法。
        # 启发式规则：
        # 1.如果正反向分词结果词数不同，则取分词数量较少的那个。
        # 2.如果分词结果词数相同 a.分词结果相同，就说明没有歧义，可返回任意一个。 b.分词结果不同，返回其中单字较少的那个。
        forward_cutlist = self.max_forward_cut(text)
        backward_cutlist = self.max_backward_cut(text)
        count_forward = len(forward_cutlist)
        count_backward = len(backward_cutlist)
    
        def compute_single(word_list):
            num = 0
            for word in word_list:
                if len(word) == 1:
                    num += 1
            return num
    
        if count_forward == count_backward:
            if compute_single(forward_cutlist) > compute_single(backward_cutlist):
                return backward_cutlist
            else:
                return forward_cutlist
    
        elif count_backward > count_forward:
            return forward_cutlist
    
        else:
            return backward_cutlist      
        
def main():
    text = '我们昨天下午上了数学课'
    tokenizer = MaxMatch('./data/dict.txt')
    print(tokenizer.max_forward_cut(text))
    print(tokenizer.max_backward_cut(text))
    print(tokenizer.max_biward_cut(text))

main()