import string
import re


class Dictionary:
    def __init__(self, files):
        self.reversed_index = {}
        self.list_files = files
        self.quant_files = 0
        for file in files:

            with open(file, encoding="utf-8") as f:
                raw = re.split("\W+", f.read().rstrip())
                words = []
                for i in range(len(raw)):
                    words.append(Dictionary.process_word(raw[i]))
                counter = 0
                # words.sort()
                for word in words:
                    index = Dictionary.get_file_index(file, files)
                    if word in self.reversed_index.keys():
                        if index not in self.reversed_index[word].keys():
                            self.reversed_index[word][index] = {counter}
                        else:
                            self.reversed_index[word][index].add(counter)
                    else:
                        self.reversed_index[word] = {index: {counter}}
                    counter += 1

                print(index, file, "with", len(words), "words")

            self.quant_files = index

    def process_word(word):
        return word.strip(string.punctuation).lower()

    def get_reversed_index(self):
        return self.reversed_index

    def get_reversed_index_word(self, word):
        if word in self.reversed_index:
            return self.reversed_index[word].keys()
        else:
            print(word, "does not exist")

    def get_matrix(self):
        for word in self.reversed_index:
            a = self.quant_files
            i = 0
            matrix = list()
            while i <= a:
                if i in self.reversed_index[word].keys():
                    matrix.append(1)
                else:
                    matrix.append(0)
                i += 1

            print(word, matrix)

    def get_matrix_word(self, word):
        if word in self.reversed_index:
            a = self.quant_files
            i = 0
            matrix = list()
            while i <= a:
                if i in self.reversed_index[word].keys():
                    matrix.append(1)
                else:
                    matrix.append(0)
                i += 1

            print(word, matrix)
        else:
            print(word, "does not exist")

    def get_file_index(file_name, list_of_files):
        return list_of_files.index(file_name)

    def boolean_search(self, request):
        # # or and not
        operation = 'NO'
        words = re.split(" +(AND|OR) +", request)
        result_set = set(self.reversed_index[words[0]].keys())
        print(words)

        for word in words:

            operation_not = False

            if word in ['AND', 'OR']:
                operation = word
                continue

            if word.find('NOT ') == 0:
                operation_not = True
                cur = word[4:]

                # print("true")

            else:
                cur = word

            if operation != 'NO':

                current_set = set(self.reversed_index[cur].keys())

                if operation == 'AND':

                    if operation_not:
                        # print("true")
                        result_set -= current_set

                    else:
                        result_set &= current_set

                elif operation == 'OR':
                    result_set |= current_set

                operation = 'NO'

            print(result_set)


dict = Dictionary(
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
# print(dict.get_matrix())

while True:

    req = input("\n\nEnter word: ")

    if req.lower() == "0":
        break

    # print(dict.get_reversed_index_word(req))
    # print(dict.get_matrix_word(req))
    print(dict.boolean_search(req))
