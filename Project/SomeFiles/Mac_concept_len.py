__author__ = 'agrawal'

import networkx as nx
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
from nltk import pos_tag
import re
import string
from simplenlp import *
from_nodes=[]
to_nodes=[]
def find_tag(sentence):
    t=pos_tag(sentence)

    return t

def create_graph():
    g=nx.DiGraph()
    with open('weight_label.txt') as f:
        content = f.read().splitlines()
    for line in content:
        words = line.split("	")
        w=int(words[2])
        from_nodes.append(words[0])
        to_nodes.append(words[1])
        g.add_edge(words[0], words[1], weight=w, label=words[3])
    return g






def main():

    file = open('obfuscated_term_enron_astar.txt', 'w')
    file_1 = open('avg_mean_enron_Astar.txt', 'w')
    G=create_graph()
    #print(from_nodes)
    #read the sentences from a given file.
    with open('sentence.txt') as f:
        lines = f.read().splitlines()
    for each_line in lines:
        #print(each_line)
        each_line=each_line.replace('\'', '')

        for c in string.punctuation:
            each_line= each_line.replace(c," ")
        line = ''.join([i for i in each_line if not i.isdigit()])
        line = re.sub("[A-Z]{2,}",'',line).replace("  ", " ")
        line=re.sub(r'\s+', ' ', line)
        line=line.lower()
        #print(line)
        sentence=line.split(" ")
        tag=find_tag(sentence)
       # print(tag)
        bag_of_words=[]
        bw=[]
        pos=[]
        list_of_mean_values=[]
        for i in range (0, len(tag)):
            #print(tag[i][0], tag[i][1])
            if tag[i][1] in ('NN', 'NNS', 'JJ', 'JJR', 'JJS', 'RBR', 'RBS'):
                if len(tag[i][0])>=2:
                    bw.append(tag[i][0])
                    pos.append(tag[i][1])
        #print(pos)
                #print(tag[i][1])
        #print('before lemma', bw)
        #pos={'NN':'n','JJ':'a','VB':'v','RB':'r', 'NNP':'n', 'NNS':'n', 'NNPS':'n', 'JJR':'a', 'JJS':'a','RBR':'r','RBS':'r', 'VBD':'v', 'VBG':'v', 'VBN':'v'}
        #print (pos)
        lmtzr = WordNetLemmatizer()
        for p in range(0, len(bw)):
            val=pos[p]
           # print(bw[p], val)
            if(val in ('NN','NNP','NNS','NNPS')):
                pos_wordnet='n'
            elif(val in ('JJ', 'JJR', 'JJS')):
                pos_wordnet='a'
            elif(val in ('RB', 'RBR', 'RBS')):
                pos_wordnet='r'
            #elif(val is ('VB', 'VBD', 'VBG', 'VBN')):
            else:
                pos_wordnet='v'
           # print(bw[p], pos_wordnet)
            lemma=lmtzr.lemmatize((bw[p]), pos_wordnet)
            #print(lemma)
            bag_of_words.append(lemma)
            #bag_of_words=['please', 'let', 'know', 'men']
        #bag of words of one sentence
        #should come under loop of each line in lines.
        #print('bag of words', bag_of_words)
        length=len(bag_of_words)
        #print(length)
        if length>1:
            for i in range (0, length):
                sen_round_i=bag_of_words.copy()
            #print('orig',sen_round_i)
                sen_round_i.pop(i)


                mean_i=[]
                len_sen_round_i=len(sen_round_i)
                #print("round", i, ": ", sen_round_i)
                k=0

                for j in range (0, len_sen_round_i-1):
                    for k in range (j, len_sen_round_i):
                        if j != k:
                            #seq1=nx.dijkstra_path(G, '/c/en/'+sen_round_i[k], '/c/en/'+sen_round_i[j])
                            #seq2=nx.dijkstra_path(G, '/c/en/'+sen_round_i[j], '/c/en/'+sen_round_i[k])
                            item1='/c/en/'+sen_round_i[j]
                            item2='/c/en/'+sen_round_i[k]
                            if ((item1 in from_nodes) or (item1 in to_nodes)) and ((item2 in from_nodes) or (item2 in to_nodes)):
                                path_one=nx.astar_path_length(G, item1, item2)
                                #nx.shortest_path_length()
                                path_two=nx.astar_path_length(G, item2, item1)
                                avg_score=(path_one+path_two)/2
                               # print (item1, item2, 'are here')
                            else:
                                #print("not in data: ", item1, item2)
                                avg_score=4
                                #print('node is not here');
                            #print(item1, item2, avg_score)
                            #nx.shortest_path_length()

                            #path_one=nx.dijkstra_path_length(G, '/c/en/'+sen_round_i[k], '/c/en/'+sen_round_i[j])
                            #path_two=nx.dijkstra_path_length(G, '/c/en/'+sen_round_i[j], '/c/en/'+sen_round_i[k])
                            #avg_score=(path_one+path_two)/2
                            #print(sen_round_i[j],',', sen_round_i[k],'>>')
                            #print(seq1)
                            #print(seq2)
                            #print('path: ', path_one, ' reverse path: ', path_two, ' average: ', avg_score)
                            mean_i.append(avg_score)

                            k=k+1;
                    #print(avg_score)
                mean_for_one_word=np.mean(mean_i)
                file_1.write(str(mean_for_one_word))
                file_1.write(", ")
                #mean_for_one_word=mean_i/len_sen_round_i
                #print('mean value: ',mean_for_one_word)
                list_of_mean_values.append(mean_for_one_word)
                sen_round_i=bag_of_words
            #index, value = max(enumerate(list_of_mean_values), key=operator.itemgetter(1))
           # print('Mean Average Conceptual Similarity: ',list_of_mean_values)
            min_value=min(list_of_mean_values)
            file_1.write('\n')
            file_1.write('\t')
            file_1.write(str(min_value))
            file_1.write('\n\n')

            index=list_of_mean_values.index(min_value)
            ot=bag_of_words[index]
            file.write(ot)
            #file.write(' ')
            file.write('\n')

            #print('obfuscated term: ', bag_of_words[index])
        else:
            file.write("NA")
            #file.write(' ')
            file.write('\n')
            file_1.write("NA")
            #file.write(' ')
            file_1.write('\n')
            #print('no target')

if __name__ == '__main__':
    main()

