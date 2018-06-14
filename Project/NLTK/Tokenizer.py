"""
Created by: Mohit Sharma

"""
import nltk


class ProcessContent:

    def __int__(self):
        pass

    # Sentence Tokenizer
    def sentence_tokenizer(self, sentence_array):

        [print("\n\nTokenized Sentence: ", nltk.word_tokenize(sentence)) for sentence in sentence_array]


sentence_Array = ["Hi this is for my Information Retrieval project"]

content = ProcessContent()
content.sentence_tokenizer(sentence_Array)

