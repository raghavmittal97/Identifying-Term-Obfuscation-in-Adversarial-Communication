"""
Created by: Mohit Sharma

"""
import sys
import nltk
import requests
from collections import OrderedDict
import time
import json
import xlsxwriter

"""
POS tag list:

CC	coordinating conjunction
CD	cardinal digit
DT	determiner
EX	existential there (like: "there is" ... think of it like "there exists")
FW	foreign word
IN	preposition/subordinating conjunction
JJ	adjective	'big'
JJR	adjective, comparative	'bigger'
JJS	adjective, superlative	'biggest'
LS	list marker	1)
MD	modal	could, will
NN	noun, singular 'desk'
NNS	noun plural	'desks'
NNP	proper noun, singular	'Harrison'
NNPS	proper noun, plural	'Americans'
PDT	predeterminer	'all the kids'
POS	possessive ending	parent's
PRP	personal pronoun	I, he, she
PRP$	possessive pronoun	my, his, hers
RB	adverb	very, silently,
RBR	adverb, comparative	better
RBS	adverb, superlative	best
RP	particle	give up
TO	to	go 'to' the store.
UH	interjection	errrrrrrrm
VB	verb, base form	take
VBD	verb, past tense	took
VBG	verb, gerund/present participle	taking
VBN	verb, past participle	taken
VBP	verb, sing. present, non-3d	take
VBZ	verb, 3rd person sing. present	takes
WDT	wh-determiner	which
WP	wh-pronoun	who, what
WP$	possessive wh-pronoun	whose
WRB	wh-abverb	where, when """

global_weight = []
global_errors = []
list_of_tags = ["VB", "VBD", "VBG", "VBP", "VBN", "VBZ", "NN", "NNS", "NNP", "JJ",
                    "RB"]  # Verb, Noun, Proper Noun, Adjective & Adverb
red_flagged_words =['federal', 'lockdown', 'dndo', 'state', 'resistant', 'bacteria', 'nuclear', 'hazmat', 'plague',
                    'canceled', 'hazardous', 'cartel', 'ebola', 'telecommunications', 'smuggling',
                    'weather', 'disaster', 'emergency', 'brush', 'cain', 'prevention', 'foot', 'conventional', 'yuma',
                    'vaccine', 'secure', 'snow', 'help', 'leak', 'reyosa', 'emergency', 'disaster', 'food', 'deaths',
                    'recruitment', 'standoff', 'execution', 'cyber', 'ms13', 'ddos', 'basque', 'malware', 'nerve',
                    'delays', 'arellano-felix', 'extremism', 'mutation', 'world', 'car', 'e.', 'swine', 'hurricane',
                    'tsunami', 'crest', 'mud', 'rootkit', 'gangs', 'communications', 'iraq', 'dock', 'collapse',
                    'tucson', 'taliban', 'recall', 'spammer', 'infrastructure', 'influenza', 'mitigation', 'nuevo',
                    'colombia', 'organized', 'decapitated', 'hezbollah', 'fundamentalism', 'watch', 'jihad',
                    'southwest', 'meth', 'recovery', 'drill', 'small', 'bridge', 'methamphetamine', 'suicide', 'gang',
                    'matamoros', 'swat', 'phreaking', 'critical', 'abu', 'bart', 'evacuation', 'iran', 'calderon',
                    'tamaulipas', 'keylogger', 'plf', 'fusion', 'michoacana', 'hamas', 'failure', 'anthrax', 'shots',
                    'trojan', 'weapons', 'enriched', 'shelter-in-place', 'dhs', 'ira', 'home', 'bomb', 'ricin',
                    'quarantine', 'electric', 'human', 'cikr', 'law', 'port', 'narcos', 'earthquake', 'black',
                    'terrorism', 'afghanistan', 'phishing', 'outbreak', 'agriculture', 'ciudad', 'interstate',
                    'bust', 'china', 'ammonium', 'shootout', 'tijuana', 'heroin', 'water/air', 'temblor', 'airplane',
                    'cocaine', 'radicals', 'closure', 'tamiflu', 'narco', 'red', 'juarez', 'sleet', 'north',
                    'salmonella', 'guzman', 'hostage', 'maritime', 'border', 'suspicious', 'marta', 'al-shabaab',
                    'plot', 'kidnap', 'la', 'reynose', 'forest', 'terror', 'sick', 'wildfire', 'plume', 'u.s.',
                    'explosion', 'breach', 'pirates', 'shooting', 'nationalist', 'blister', 'trafficking', 'crash',
                    'industrial', 'avian', 'tamil', 'worm', 'drug', 'los', 'agent', 'consular', 'relief', 'hail',
                    'warning', 'immigration', 'alcohol', 'biological', 'artistics', 'extreme', 'authorities',
                    'gunfight', 'erosion', 'avalanche', 'aid', 'incident', 'grid', 'environmental', 'flu', 'denial',
                    'department', 'strain', 'fort', 'lightening', 'flood', 'smart', 'assassination', 'islamist',
                    'marijuana', 'san', 'sinaloa', 'conficker', 'twister', 'mexicles', 'el', 'amtrak', 'riot',
                    'violence', 'eta', 'nigeria', 'mysql', 'tuberculosis', 'air', 'homeland', 'body', 'brown',
                    'looting', 'exposure', 'burn', 'h1n1', 'ttp', 'threat', 'cloud', 'mexico', 'torreon', 'nogales',
                    'service', 'power', 'burst', 'brute', 'pipe', 'transportation', 'blizzard', 'metro', 'police',
                    'center', 'epidemic', 'agro', 'pork', 'mara', 'aqim', 'barrio', 'narcotics', 'domestic',
                    'pakistan', 'somalia', 'improvised', '2600', 'typhoon', 'computer', 'infection', 'ied', 'national',
                    'task', 'subway', 'contamination', 'attack', 'exercise', 'new', 'eco', 'aqap', 'radiation',
                    'customs', 'facility', 'pandemic', 'coast', 'stranded/stuck', 'botnet', 'yemen', 'security',
                    'response', 'powder', 'sarin', 'health', 'first', 'sonora', 'public', 'al', 'antiviral',
                    'beltran-leyva', 'wave', 'screening', 'plo', 'symptoms', 'central', 'viral', 'cops', 'tremor',
                    'tornado', 'social', 'listeria', 'magnitude', 'wmata', 'illegal', 'united', 'ice', 'secret',
                    'virus', 'dirty', 'militia', 'nbic', 'h5n1', 'farc', 'toxic', 'storm', 'mexican', 'spillover',
                    'scammers', 'hazmat', 'radioactive', 'gulf', 'airport', 'gas', 'target', 'norvo', 'chemical',
                    'hacker']
red_flag_sentence_report = []
json_return = []
json_dict = {}
red_flag_count = -1
temp_arr = []
excel_count = 0


class ProcessContent:
    global global_weight, global_errors, list_of_tags, red_flag_sentence_report, input_sentence, red_flag_count, excel_count
    result_to_excel = [""]
    red_flag_count += 1
    tokens = ""
    tagged_tokens = ""
    bow = []
    list_of_weights = []
    sentence_number = 0
    input_sentence = ''
    def __int__(self):
        pass

    # Sentence Tokenizer
    def sentence_tokenizer(self, sentence):
        global tokens, input_sentence
        input_sentence = sentence
        ProcessContent.result_to_excel.append(input_sentence)
        # [print("Tokenized Sentence: ", nltk.word_tokenize(sentence)) for sentence in sentence_array]
        tokens = [nltk.word_tokenize(sentence)]
        print(tokens)
        # print("\nTokenized Sentence:", *tokens)

    # Sentence Tagger
    def sentence_tagger(self):
        global tagged_tokens
        tagged_tokens = [nltk.pos_tag(token) for token in tokens]
        # print('Tokens: ', *tagged_tokens)

    # Bag of Words
    def bag_of_words(self):
        global tagged_tokens, input_sentence, list_of_tags

        for each_token in tagged_tokens:
            for token, tag in each_token:
                if tag in list_of_tags and len(token) > 2:
                    ProcessContent.bow.append(token)
        bow = list(set(ProcessContent.bow))
        ProcessContent.result_to_excel.append(bow)
        for word in bow:
            if word in red_flagged_words:
                red_flag_sentence_report.append((word, input_sentence))

        # print('Bag of Words: ', bow)

    # Lemmatization
    def lemmatizer(self):
        global tokens
        tokens = [nltk.WordNetLemmatizer().lemmatize(token, pos='v') for token in ProcessContent.bow]
        if 'be' in tokens:
            tokens.remove('be')
        print('Lemmatized Tokens: ', tokens)

    # # Stemming
    # def stemmer(self):
    #     global tokens
    #     tokens = [nltk.PorterStemmer().stem(token) for token in tokens]
    #     print('\n Stemmed Tokens: ', tokens)

    # Using ConceptNetAPI to find distance between BOW
    def conceptAPI(self):
        global tokens, global_weight, global_errors, input_sentence, red_flagged_words, red_flag_sentence_report
        ProcessContent.sentence_number += 1
        weight_for_term_combination = OrderedDict()
        count = -1
        if len(tokens) > 2:
            for each_token in tokens:
                # print("\n|| " + each_token + " ||")
                # print("="*(len(each_token)+6))
                # weights = 0
                for token in tokens:
                    if token != each_token:

                        # Extracting the weight between two terms
                        test = (requests.get(
                            'http://api.conceptnet.io/related/c/en/' + token + '?filter=/c/en/' + each_token).json())
                        # print((test['related'][0]['@id'][6:]), test['@id'][6:], test['related'][0]['weight'])

                        # testing if weight is null
                        if not test['related']:
                            print("ConceptNet doesn't have " + token + " & " + each_token + " as nodes in it's graph")
                            global_errors.append((each_token, token))
                            break
                        # weights += test['related'][0]['weight']
                        # print(weights)
                        # Extracting unique term-weight combinations

                        first_word = each_token
                        second_word = token
                        weight = test['related'][0]['weight']

                        # ProcessContent.list_of_weights = [(first_word, second_word, weight)]
                        # weight_for_term_combination('0':first_weight, '1':second_weight, ...)

                        if (not (first_word, second_word, weight) in ProcessContent.list_of_weights) and (
                                not (second_word, first_word, weight) in ProcessContent.list_of_weights):
                            # count += 1
                            ProcessContent.list_of_weights.append((first_word, second_word, weight))
                            # weight_for_term_combination[str(count)] = weight

        # Finding Max weight difference in BoW per line.
        if len(ProcessContent.list_of_weights) > 0:
            print(*ProcessContent.list_of_weights)
            # bow with weights
            ProcessContent.result_to_excel.append(ProcessContent.list_of_weights)
            # max_key = max(weight_for_term_combination, key=lambda k: weight_for_term_combination[k])

            # Scaling BoW > 3
            # Calculating weights for each term from the rest of the terms.
            term_weight_score = {}
            term_weight_score_without_sum = {}
            for term in tokens:
                weights_score_of_rest_of_the_terms = []
                count = 0
                for combination_weight in ProcessContent.list_of_weights:
                    if term not in combination_weight:
                        count += 1
                        weights_score_of_rest_of_the_terms.append(combination_weight[2])
                term_weight_score_without_sum[term] = weights_score_of_rest_of_the_terms
                term_weight_score[term] = sum(weights_score_of_rest_of_the_terms)/count

            # term weight score / Oddity to excel
            ProcessContent.result_to_excel.append(term_weight_score)

            # print('\n', term_weight_score_without_sum, '\n')
            print('Term Weight Score(Summed): ', term_weight_score)
            max_key = max(term_weight_score, key=lambda k: term_weight_score[k])
            print("Obfuscated Term: ", "|| " + max_key + " ||")

            # obfuscated term to excel
            ProcessContent.result_to_excel.append(max_key)
            # red flagged term to excel


            json_dict['sentence'] = input_sentence
            json_dict['Obfuscated_Term'] = max_key
            if red_flag_sentence_report:
                json_dict['Red_Flagged'] = red_flag_sentence_report[0][0]
                ProcessContent.result_to_excel.append(red_flag_sentence_report[0][0])
            else:
                json_dict['Red_Flagged'] = ""
                ProcessContent.result_to_excel.append("")
            # # Extracting the Obfuscated Term for Bow < 3
            # # for term in ProcessContent.bow:
            # for term in tokens:
            #     # cross checking key with max weight in list_of_weights list.
            #     if not term in ProcessContent.list_of_weights[int(max_key)]:
            #         print("Obfuscated Term: ", "|| " + term + " ||")
            #         pass

            # print(ProcessContent.list_of_weights)
            # print(weight_for_term_combination)
            list_of_weight = list(map(lambda k: term_weight_score[k], term_weight_score))
            # print(list_of_weight)
            max_weight = max(list_of_weight)
            # print(max_weight)
            weight_differences = list(map(lambda each_weight: max_weight - each_weight, list_of_weight))
            weight_differences.remove(0.0)
            # print(weight_differences)
            max_weight_diff = max(weight_differences)
            print('Max Difference: ', max(weight_differences))
            global_weight.append(max_weight_diff)
            # print("Max Weight: ", max_weight, 'Min Weight: ', min_weight)
            # print('Max Difference: ', max_weight-min_weight)
            # print(max_key-min_key)
            print('\n')
        else:
            # print("\n")
            print("Sentence is semantically correct.\n")
            json_dict['sentence'] = input_sentence
            json_dict['Obfuscated_Term'] = 'Sentence is semantically correct'

            if red_flag_sentence_report:
                json_dict['Red_Flagged'] = red_flag_sentence_report[0][0]
                ProcessContent.result_to_excel.append(red_flag_sentence_report[0][0])
            else:
                json_dict['Red_Flagged'] = ""
                ProcessContent.result_to_excel.append("")

            ProcessContent.result_to_excel.append("")
            ProcessContent.result_to_excel.append("")
            ProcessContent.result_to_excel.append('Sentence is semantically correct')


        ProcessContent.bow = []
        ProcessContent.list_of_weights = []
        t = ProcessContent()
        t.write_to_excel(ProcessContent.result_to_excel)
    def write_to_excel(self, results):
        global excel_count
        excel_count +=1
        # Create an new Excel file and add a worksheet.
        normal_sentence = results[0]
        obfuscated_sentence = results[1]
        bow = results[2]
        bow = ','.join(bow)
        temp_str = []
        bow_with_weights = results[3]
        for i in bow_with_weights:
            temp_str.append(i[0]+' '+ i[1]+ ' '+ str(i[2]))
        bow_with_weights = ','.join(temp_str)
        temp_str = []
        bow_with_oddity = results[4]
        for i in bow_with_oddity:
            temp_str.append(i+' '+str(bow_with_oddity[i]))
        bow_with_oddity = ','.join(temp_str)
        obfuscated_term = results[5]
        red_flagged = results[6]

        workbook = xlsxwriter.Workbook('results.xlsx')
        worksheet = workbook.add_worksheet()

        # Widen the first column to make the text clearer.
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 30)
        worksheet.set_column('F:F', 30)
        worksheet.set_column('G:G', 20)

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Write some simple text.
        worksheet.write('A1', 'Normal Text', bold)
        worksheet.write('B1', 'Obfuscated Text', bold)
        worksheet.write('C1', 'Bag of Words', bold)
        worksheet.write('D1', 'Bag of Words with weights', bold)
        worksheet.write('E1', 'Bag of Words with Oddity Score', bold)
        worksheet.write('F1', 'Obfuscated term', bold)
        worksheet.write('G1', 'Red_flagged', bold)

        worksheet.write(excel_count, 0, normal_sentence)
        worksheet.write(excel_count, 1, obfuscated_sentence)
        worksheet.write(excel_count, 2, bow)
        worksheet.write(excel_count, 3, bow_with_weights)
        worksheet.write(excel_count, 4, bow_with_oddity)
        worksheet.write(excel_count, 5, obfuscated_term)
        worksheet.write(excel_count, 6, red_flagged)

        workbook.close()

    def run(self, input_sentence):
        global json_dict, json_return, temp_arr, red_flag_sentence_report, red_flagged_words
        # User Input
        # input_file = 'test_input.txt'
        start = time.time()
        # input_file = sys.argv[1]
        # input_file = 'test_input.txt'

        input_sentence = input_sentence.replace('%', ' ')
        input_sentence = input_sentence.replace('20', ' ')

        input_sentence = [input_sentence]
        sentence_Array = []
        for line in input_sentence:
            line = line.lower()
            sentence_Array += line.split(".")

        # filtering out empty elements
        # sentence_Array = list(filter(None, sentence_Array))

        # Tokenizing each word in each sentence to find duplicates
        sentence_Array = [nltk.word_tokenize(each_sentence) for each_sentence in sentence_Array]

        # Removing duplicate elements
        new_sentence_array = []
        for each_sentence in sentence_Array:
            result = []
            for each_word in each_sentence:
                if each_word not in result:
                    result.append(each_word)

            result = ' '.join(result)
            if result not in new_sentence_array:
                new_sentence_array.append(result)

        sentence_Array = new_sentence_array

        # filtering out empty elements
        sentence_Array = list(filter(None, sentence_Array))
        print('Number of Lines: ', len(sentence_Array))
        [print('"' + line + '"') for line in sentence_Array]
        print('\n')
        line_count = 1
        for each_line in sentence_Array:
            print((len(sentence_Array)-line_count), 'lines remaining')
            print('"' + each_line + '"')
            content = ProcessContent()
            content.sentence_tokenizer(each_line)
            content.sentence_tagger()
            content.bag_of_words()
            content.lemmatizer()
            # content.stemmer()
            content.conceptAPI()
            print(type(json_return))
            # json_return.append(json_dict)
            temp_arr.append(json_dict)
            line_count += 1

        json_return = json.dumps(temp_arr)
        temp_arr = []
        red_flag_sentence_report = []
        red_flagged_words = []
        print(json_return)
        return json.loads(json_return)



        # Writing the result to a file
        with open('/home/m_academic/Desktop/Avg_weight_test', 'a') as f:
            f.write('+'*159)
            f.write('\n\n\n')
            f.write('Max_Differences: ')
            for w in global_weight:
                f.write(str(w))
            try:
                f.write('\nAverage Max Weight Difference: '+ str(sum(global_weight)/len(global_weight)))
            except:
                print("Semantically correct sentence.")
            if not red_flag_sentence_report:
                for w in red_flag_sentence_report:
                    f.write('\nRed Flagged Sentences: '+w)
            f.write('\nNo Connected nodes between: ')
            for e in global_errors:
                f.write(str(e))
            f.write('\n')

        print('Max_weight Differences: ', global_weight)
        try:
            print('Average Max Weight Difference: ', sum(global_weight)/len(global_weight))
        except:
            print("Semantically correct sentence.")

        if global_errors:
            print('No Connected nodes between: ', *global_errors)
        if red_flag_sentence_report:
            print('Red Flagged Sentences: ')
            for word in red_flag_sentence_report:
                word = ' - '.join(word)
                print('\t', word)

        t = time.time() - start
        print("Time Elapsed: --- %s seconds ---" % (round(t, 3)))


t = ProcessContent()
t.run('Pen will be delivered to shoot the president')
