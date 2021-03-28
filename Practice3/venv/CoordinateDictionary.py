import string
import re
import jgraph
import math


class CoordinateDictionary:
    def __init__(self, files):
        self.reversed_index = {}
        self.list_files = files
        self.quant_files = 0
        for file in files:

            with open(file, encoding="utf-8") as f:
                raw = re.split("\W+", f.read().rstrip())
                words = []
                for i in range(len(raw)):
                    words.append(CoordinateDictionary.process_word(raw[i]))
                position = 0

                # words.sort()
                for word in words:
                    # counter = 0
                    # index = CoordinateDictionary.get_file_index(file, files)
                    # if word in self.reversed_index.keys():
                    #     if index not in self.reversed_index[word].keys():
                    #         self.reversed_index[word][index] = {position}
                    #     else:
                    #         self.reversed_index[word][index].add(position)
                    # else:
                    #     self.reversed_index[word] = {index: {position}}
                    # position += 1
                    index = CoordinateDictionary.get_file_index(file, files)
                    if word in self.reversed_index.keys():
                        self.reversed_index[word][0] = self.reversed_index[word][0] + 1
                        if index in self.reversed_index[word][1]:
                            self.reversed_index[word][1][index].append(position)
                        else:
                            self.reversed_index[word][1][index] = [position]
                    else:
                        self.reversed_index[word] = []
                        self.reversed_index[word].append(1)
                        self.reversed_index[word].append({})
                        self.reversed_index[word][1][index] = [position]
                    position += 1

                print(index, file, "with", len(words), "words")

            self.quant_files = index

    def process_word(word):
        return word.strip(string.punctuation).lower()

    def get_reversed_index(self):
        return self.reversed_index

    def get_file_index(file_name, list_of_files):
        return list_of_files.index(file_name)

    def search(self, request):

        raw = re.split("\W+", request.rstrip())
        words = []
        for i in range(0, len(raw)):
            words.append(CoordinateDictionary.process_word(raw[i]))
        print(words)

        # 0 words
        if len(words) == 0:
            return {}
        # 1 word
        if len(words) == 1:
            if words[0] in self.reversed_index:
                return self.reversed_index[words[0]]
            return {}

        if words[0] not in self.reversed_index.keys():
            return {}
        res = []
        if words[1].isnumeric:
            if words[0] in self.reversed_index:
                if words[2] in self.reversed_index:
                    num = int(words[1])
                    for k in self.reversed_index[words[0]][1].keys():
                        for i in self.reversed_index[words[0]][1][k]:
                            if k in self.reversed_index[words[2]][1].keys():
                                for j in self.reversed_index[words[2]][1][k]:
                                    check = math.fabs(j - i)
                                    if check <= num+1:
                                        if not res.__contains__(k):
                                            res.append({k,i,j})
                            else:
                                return res
        return res


dict = CoordinateDictionary(
    ["library/alice.txt",
     "library/frankenstein.txt",
     "library/gogol.txt",
     "library/hamlet.txt",
     "library/kafka.txt",
     "library/peterpan.txt",
     "library/romeo.txt",
     "library/tempest.txt",
     "library/treasure.txt",
     "library/wells.txt"])

print(len(dict.get_reversed_index().keys()), "unique words")
# print(dict.get_reversed_index())

while True:

    req = input("\n\nEnter word: ")

    if req.lower() == "0":
        break
    print(dict.search(req))
