
import time
import string
import re
import os


class PermutermIndex:
    def process_word(word):
        return word.strip(string.punctuation).lower()

    def __init__(self, folder):
        list_of_files = [os.path.join(folder, f) for f in os.listdir(folder) if
                         os.path.isfile(os.path.join(folder, f))]
        self.terms = {}
        self.inverted_index = {}
        for file_name in list_of_files:
            start = time.process_time()
            with open(file_name, encoding="utf-8") as file:
                for word in re.split("\W+", file.read().rstrip()):
                    w = PermutermIndex.process_word(word)
                    if not w or not len(w):
                        continue
                    if w in self.inverted_index.keys():
                        self.inverted_index[w].add(file_name)
                    else:
                        self.inverted_index[w] = {file_name}
                    for i in {'$' + w} | {w[i:] + '$' + w[:i] for i in range(len(w))}:
                        if i in self.terms.keys():
                            self.terms[i].add(w)
                        else:
                            self.terms[i] = {w}
            end = time.process_time()
            print(file_name, "done in", end - start, "s")

    def joker_search(self, req):
        joker = req.count('*')

        if joker == 0:
            matching_words = set()
            for i in [self.terms[k] for k in self.terms.keys() if (req + '$' in k or '$' + req in k)]:
                matching_words |= i
            print(matching_words)
            res = {}
            for i in matching_words:
                if i in self.inverted_index.keys():
                    res[i] = self.inverted_index[i]

            return res

        if joker == 1:
            q = ""
            for i in range(len(req)):
                if req[i] != '*':
                    q += req[i]
                else:
                    q = req[i + 1:].lower() + '$' + q.lower()
                    break

            matching_words = set()
            for i in [self.terms[k] for k in self.terms.keys() if k.startswith(q)]:
                matching_words |= i
            res = {}
            for i in matching_words:
                if i in self.inverted_index.keys():
                    res[i] = self.inverted_index[i]
            return res

        if joker >= 2:
            f = req.find('*')
            q1 = req[:f].lower()

            mid = []
            while True:
                f1 = req.find('*', f + 1)
                if f1 == -1:
                    q2 = req[f + 1:].lower()
                    break
                mid.append(req[f + 1:f1].lower())
                f = f1

            q = q2 + '$' + q1
            matching_words = set()
            for i in [self.terms[k] for k in self.terms.keys() if k.startswith(q)]:
                for j in i:
                    to_add = True
                    pos = -1
                    for k in mid:
                        if k not in j or j.find(k, pos + 2) == -1:
                            to_add = False
                            break
                        pos = j.find(k, pos + 2)
                    if to_add:
                        matching_words |= i
            # print(matching_words)
            res = {}
            for i in matching_words:
                if i in self.inverted_index.keys():
                    res[i] = self.inverted_index[i]
            return res


if __name__ == "__main__":
    ind = PermutermIndex("library")
    print(ind.terms)
    while True:
        query = PermutermIndex.process_word(input("\n\nEnter request: "))
        if PermutermIndex.process_word(query) == "exit":
            break
        print(ind.joker_search(query))
    # print(ti.terms)
