# Author: Ma, Shoujiang
# Data: 2/20/2018
# Describe: Build a dictionary based on my own needs.

import os.path
import re

import pandas as pd


class Dictionary(object):
    def __init__(self, dic_name):
        if not os.path.isfile(dic_name):
            open(dic_name, 'a').close()
        self.total_words = 0
        self.dic_name = dic_name
        try:
            self.dic = pd.read_csv(dic_name, squeeze=True, header=None)
        except pd.io.common.EmptyDataError:
            self.dic = pd.Series(dtype=str)

    def read_text(self, file_name):
        with open(file_name, 'r') as file:
            self.extract_words(file)

    def extract_words(self, file):
        words = []
        while True:
            line = file.readline()
            if not line:
                break
            pattern = '[a-zA-Z]+'
            line = re.findall(pattern, line)  # default split is space

            # search if in Dic already.
            for word in line:
                if not self.word_exist(word):
                    words.append(word)

        words = self.delete_duplicate(words)
        self.to_dic(words)

    def delete_duplicate(self, words):
        new_words = list(set(words))
        return new_words

    def word_exist(self, word):
        return True if self.dic[self.dic == word].size else False

    def to_dic(self, words):
        df = pd.Series(words)
        df.to_csv(self.dic_name, mode='a+', header=False, index=False)

    def get_words_frequency(self):
        pass

    def sort(self):
        pass


if __name__ == '__main__':
    dic_name = './Dictionary.csv'
    dic = Dictionary(dic_name)
    file_name = './text.txt'
    dic.read_text(file_name)
