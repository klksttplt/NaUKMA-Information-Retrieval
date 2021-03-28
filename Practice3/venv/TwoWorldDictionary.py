import string
import re

class TwoWordDictionary:
    def __init__(self, files):
        self.reversed_index = {}
        self.list_files = files
        self.quant_files = 0
        for file in files:
            with open(file, encoding="utf-8") as f:
                raw = re.split("\W+", f.read().rstrip())
                combs = []
                for i in range(1, len(raw)):
                    # words.sort()
                    combs.append(
                        TwoWordDictionary.process_word(raw[i - 1]) + ' ' + TwoWordDictionary.process_word(raw[i]))
                for word in combs:
                    index = TwoWordDictionary.get_file_index(file, files)
                    if word in self.reversed_index.keys():
                        if index not in self.reversed_index[word]:
                            self.reversed_index[word].add(index)
                    else:
                        self.reversed_index[word] = {index}

                print(index, file, "with", len(combs) + 1, "combs")

            self.quant_files = index

    def process_word(word):
        return word.strip(string.punctuation).lower()

    def get_file_index(file_name, list_of_files):
        return list_of_files.index(file_name)

    def get_reversed_index(self):
        return self.reversed_index

    def search(self, request):
        raw = re.split("\W+", request.rstrip())
        combs = []
        for i in range(1, len(raw)):
            combs.append(
                TwoWordDictionary.process_word(raw[i - 1]) + ' ' + TwoWordDictionary.process_word(raw[i]))
        # 0 words
        if len(combs) == 0:
            return {}
        # 1 word
        if len(combs) == 1:
            if combs[0] in self.reversed_index.keys():
                return set(self.list_files[x] for x in self.reversed_index[combs[0]])
            return {}

        if combs[0] not in self.reversed_index.keys():
            return {}
        res = self.reversed_index[combs[0]]
        for i in range(1, len(combs)):
            if combs[i] not in self.reversed_index.keys():
                return {}
            res = res & self.reversed_index[combs[i]]
            if not len(res):
                return {}
        return set(self.list_files[x] for x in res)



twd = TwoWordDictionary(
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

print(len(twd.get_reversed_index().keys()), "unique words")
print(twd.get_reversed_index())

while True:
    req = input("\n\nEnter the request: ")
    if req.lower() == "0":
        break
    print(twd.search(req))