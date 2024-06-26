# Script zum generieren eines dictionaries mit fragen (keys) und einer liste von
# falschen antworten, die per Konsole eingegeben werden, zur passenden frage (value)
# das Dictionary wird als .json Datei gespeichert. Bei erneuter Eingabe wird
# geprüft ob besagte .json Datei vorhanden ist und schon beanwortete Fragen werden
# übersprungen

import json, os, converter

# load our questions from data.json
with open('data.json') as json_data:
    qa_dict = json.load(json_data)

# check if we already have some saved data
if os.path.isfile('false.json'):
    with open('false.json') as json_false:
        false_answers = json.load(json_false)
else:
    false_answers = {}

active = True
questions = list(qa_dict.keys())
userinput = ''

while active:

    for question in questions:
        # if question has been already answered, skip it
        if question in false_answers:
            continue

        false_list = []
        print('Nächste Frage:')
        print(question)

        # input 4 wrong answers
        for i in range(3):
            false_answer = input('Geben sie die falsche Antwort ein: ')
            false_list.append(false_answer)

        # update our dictionary
        false_answers.update({question: false_list})
        converter.make_json(false_answers,'','false.json')

        userinput = input('Weitere Frage bearbeiten? (j)a/(n)ein: ')
        if userinput == 'n':
            active = False
            break




    