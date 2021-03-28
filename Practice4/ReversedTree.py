
import time
import string
import re
import os


class Node:
    def __init__(self, char, files=None):
        self.letter = char
        self.files = files
        self.children = {}

    def __str__(self):
        return self.children


class Reversed_Tree:


    def process_word(word):
        return word.strip(string.punctuation).lower()

    def add_word(self, w, file):
        if not w or not len(w):
            return
        if w[0] not in self.nodes.keys():
            self.nodes[w[0]] = Node(w[0])
        cur_node = self.nodes[w[0]]
        for i in range(1, len(w)):
            if w[i] not in cur_node.children.keys():
                cur_node.children[w[i]] = Node(w[i])
            cur_node = cur_node.children[w[i]]
        if not cur_node.files:
            cur_node.files = {file}
        else:
            cur_node.files.add(file)

    def search(self, word):
        if not word or not len(word):
            return False
        if word[0] not in self.nodes.keys():
            self.nodes[word[0]] = Node(word[0])
        cur_node = self.nodes[word[0]]
        for i in range(1, len(word)):
            if word[i] not in cur_node.children.keys():
                return False
            cur_node = cur_node.children[word[i]]
        return cur_node.files

    def __init__(self, file_folder):
        files = [f for f in os.listdir(file_folder) if os.path.isfile(os.path.join(file_folder, f))]
        self.nodes = {}
        for file_name in files:
            start = time.process_time()

            with open(os.path.join(file_folder, file_name), encoding="utf-8") as file:
                words = {Reversed_Tree.process_word(w) for w in re.split("\W+", file.read().rstrip())}
                for w in words:
                    self.add_word(w, file_name)
            end = time.process_time()
            print(file_name, "done in", end - start, "s")


if __name__ == "__main__":
    rt = Reversed_Tree("library")

    while True:
        req = input("\n\nEnter word: ")
        if req.lower() == "0":
            break
        print(rt.search(Reversed_Tree.process_word(req)))