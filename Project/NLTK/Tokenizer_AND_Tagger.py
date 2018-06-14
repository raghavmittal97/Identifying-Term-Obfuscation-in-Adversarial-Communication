"""
Created by: Mohit Sharma

"""
import nltk


class ProcessContent:

    tokens = ""

    def __int__(self):
        pass

    # Sentence Tokenizer
    def sentence_tokenizer(self, sentence_array):
        global tokens
        tokens = [nltk.word_tokenize(sentence) for sentence in sentence_array]
        print("\n\nTokenized Sentence:", *tokens)

    # Sentence Tagger
    def sentence_tagger(self):
        tagged_tokkens = [nltk.pos_tag(token) for token in tokens]
        print("\n\nTagged Tokkens: ", *tagged_tokkens)


sentence_Array = ["Hi this is for my Information Retrieval project"]

content = ProcessContent()
content.sentence_tokenizer(sentence_Array)
content.sentence_tagger()
