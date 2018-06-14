"""
Created by: Mohit Sharma
"""
import re
import random
import xlsxwriter
import nltk
from collections import OrderedDict

noun_words = []
list_of_tags = ["VB", "VBD", "VBG", "VBP", "VBN", "VBZ", "NN", "NNS", "NNP", "JJ", "RB"]
# get list of nouns from the file
with open('nouns.txt', 'r') as f:
    for line in f:
        line = line.replace("    ", "")
        line = line.replace("\n", "")
        noun_words.append(line)
    noun_words = [item for item in noun_words if item != '']
    # print(noun_words)
    len_noun_words = len(noun_words)

# get list of sentences from the essay
with open('original.txt', 'r+') as f:
    original_sentence = OrderedDict()
    count = 0
    # getting the input in the right format
    for line in f:
        splitted = re.split("[.]", line)
        splitted = [item for item in splitted if len(item.split()) > 9]

        for l in splitted:
            if not l == "":
                original_sentence[count] = l
                count += 1
    # print(original_sentence)

    original_sentence = {i: j for i, j in original_sentence.items() if len(j) > 1}
    copy_original_sent = original_sentence
    changed_sentence = OrderedDict()
    nouns_used = OrderedDict()
    original_word = OrderedDict()

    # print(copy_original_sent)

    count = 0
# replace a noun in the sentence with a random noun
    for key, value in copy_original_sent.items():
        if len(value) > 4:
            value = value.lstrip(" ")
            value = ([value])
            value = value[0].split()
            # print(value)
            length = len(value)

            bow = []

            # find index of noun in the sentence -"value"
            # tokenize line
            value = ' '.join(value)
            tokens = [nltk.word_tokenize(value)]
            # tagging tokens
            tagged_tokens = [nltk.pos_tag(token) for token in tokens]
            # getting BOW
            for each_token in tagged_tokens:
                for token, tag in each_token:
                    if tag in list_of_tags and len(token) > 2:
                        bow.append(token)
            bow = list(set(bow))

        # print(len(bow))
        value = value.replace(",", "")
        value = value.split()
        # finding index of noun in bow of the sentence - "value"
        try:
            random_bow_index = random.randrange(0, len(bow)-1)
            # print(value)
            # print(bow[random_bow_index])
            # print(value.index(bow[random_bow_index]))
            noun_index = value.index(bow[random_bow_index])
            while len(value[noun_index]) <= 3:
                random_bow_index = random.randrange(0, len(bow) - 1)
                noun_index = value.index(bow[random_bow_index])
            # print(noun_index)
            #
            # print(value[noun_index])
            random_noun = random.randrange(0, len_noun_words)
            original_word[count] = value[noun_index]
            value[noun_index] = noun_words[random_noun]
            changed_sentence[key] = ' '.join(value)
            nouns_used[key] = noun_words[random_noun]
            count += 1
        except:
            print("")
            pass


print(original_sentence)
print(changed_sentence)
print(nouns_used)


# writing to excel sheet.
workbook = xlsxwriter.Workbook('Database.xlsx')
worksheet = workbook.add_worksheet()

# Widen the first column to make the text clearer.
worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 20)
worksheet.set_column('C:C', 20)


# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})

# Write some simple text.
worksheet.write('A1', 'Normal Text', bold)
worksheet.write('B1', 'Obfuscated Text', bold)
worksheet.write('C1', 'Original Word', bold)
worksheet.write('D1', 'Obfuscated Word', bold)

num_of_items_in_dic = max(changed_sentence, key=int)


for i in range(0, num_of_items_in_dic):
    try:
        worksheet.write(i, 0, original_sentence[i])
        worksheet.write(i, 1, changed_sentence[i])
        worksheet.write(i, 2, original_word[i])
        worksheet.write(i, 3, nouns_used[i])
    except:
        pass

workbook.close()
