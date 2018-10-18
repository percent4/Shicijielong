import re
import pickle
from xpinyin import Pinyin
from collections import defaultdict

def main():
    with open('F://poem.txt', 'r') as f:
        poems = f.readlines()

    sents = []
    for poem in poems:
        parts = re.findall(r'[\s\S]*?[。？！]', poem.strip())
        for part in parts:
            if len(part) >= 5:
                sents.append(part)

    poem_dict = defaultdict(list)
    for sent in sents:
        print(part)
        head = Pinyin().get_pinyin(sent, tone_marks='marks', splitter=' ').split()[0]
        poem_dict[head].append(sent)

    with open('./poemDict.pk', 'wb') as f:
        pickle.dump(poem_dict, f)

main()