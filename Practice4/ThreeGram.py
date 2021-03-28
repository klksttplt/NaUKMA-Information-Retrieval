
import time
import string
import re
import os


class ThreeGram:

    def __init__(self, folder):
        files = [os.path.join(folder, f) for f in os.listdir(folder) if
                         os.path.isfile(os.path.join(folder, f))]
        self.threegrams = {}
        self.index = {}
        for file in files:
            start = time.process_time()
            with open(file, encoding="utf-8") as f:
                for w in re.split("\W+", f.read().rstrip()):
                    g = ThreeGram.get_threegrams(w)
                    word = ThreeGram.process_word(w)
                    if not g:
                        continue
                    # if word:
                    #     if word in self.index.keys():
                    #         self.index[word].add(file)
                    #     else:
                    #         self.index[word] = {file}
                    for i in g:
                        if i in self.threegrams.keys():
                            self.threegrams[i].add(word)
                        else:
                            self.threegrams[i] = {word}
            end = time.process_time()
            print(file, "done in", end - start, "s")
        print(self.threegrams)

    def process_word(word):
        return word.strip(string.punctuation).lower()

    def get_threegrams(word):
        w = ThreeGram.process_word(word)
        if not w or not len(w) or len(w) == 1:
            return None
        if len(w) == 2:
            return {'$' + w} | {w + '$'}
        res = {'$' + w[:2]} | {w[len(w) - 2:] + '$'}
        for i in range(len(w) - 2):
            res.add(w[i:i + 3])
        return res



if __name__ == "__main__":
    tg = ThreeGram("library")