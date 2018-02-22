# -*- coding:utf-8 -*-
# Author: Ma, Shoujiang
# Data: 2/20/2018
# Describe: Build a dictionary based on my own needs.

import hashlib
import json
import os.path
import re
import time
import urllib
import urllib2

import pandas as pd


class Dictionary(object):
    def __init__(self, dic_name):
        if not os.path.isfile(dic_name):
            open(dic_name, 'a').close()

        self.total_words = 0
        self.dic_name = dic_name
        self.columns = ['英', '汉']

        self.url = 'http://fanyi.youdao.com/translate?' \
                   'smartresult=dict&smartresult=rule'

        try:
            self.dic = pd.read_csv(dic_name)
        except pd.io.common.EmptyDataError:
            self.dic = pd.DataFrame(columns=self.columns, dtype=str)
            self.dic.to_csv(self.dic_name, encoding="utf-8", index=False)

    def read_text(self, file_name):
        with open(file_name, 'r') as file:
            self.extract_words(file)

    def extract_words(self, file):
        words = []
        while True:
            line = file.readline()
            line = line.lower()
            if not line:
                break
            pattern = '[a-zA-Z]+'
            line = re.findall(pattern, line)  # default split is space

            # search if in Dic already.
            for word in line:
                if not self.word_exist(word):
                    words.append(word)
        words = self.delete_duplicate(words)
        word_mean = self.zip_word_and_mean(words)
        self.to_dic(word_mean)

    def word_exist(self, word):
        return True if self.dic['英'][self.dic['英'] == word].size else False

    def delete_duplicate(self, words):
        new_words = list(set(words))
        return new_words

    def zip_word_and_mean(self, words):
        meanings = []
        for word in words:
            meaning = self.translate(word)
            meanings.append(meaning)
        return zip(words, meanings)

    def to_dic(self, words):
        df = pd.DataFrame(words, columns=self.columns)
        df.to_csv(self.dic_name, mode='a', encoding="utf-8", header=False, index=False)

    def translate(self, input):
        data = self.form_data(input)
        data = urllib.urlencode(data)
        request = urllib2.Request(self.url, data=data)
        response = urllib2.urlopen(request)
        html = response.read()
        target = json.loads(html)
        result = target["translateResult"][0][0]['tgt']
        return result

    def form_data(self, input):
        salt = str(int(time.time() * 1000))
        client = 'fanyideskweb'
        a = "rY0D^0'nM0}g5Mm1z%1G4"
        md5 = hashlib.md5()
        digStr = client + input + salt + a
        md5.update(digStr)
        sign = md5.hexdigest()

        data = {}
        data['i'] = input
        data['from'] = 'AUTO'
        data['to'] = 'AUTO'
        data['smartresult'] = 'dict'
        data['client'] = 'fanyideskweb'
        data['salt'] = salt
        data['sign'] = sign
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['action'] = 'FY_BY_CLICKBUTTION'
        data['typoResult'] = 'false'
        return data


if __name__ == '__main__':
    dic_name = './Dictionary.csv'
    dic = Dictionary(dic_name)
    file_name = './text.txt'
    dic.read_text(file_name)
