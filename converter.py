# Script zum einlesen einer Anzahl von .docx Dokumenten die Fragen und Antworten
# enthalten und Anlegen einer .json Datei, welche Fragen als Keys und zugehörige 
# Antworten als Value enthält

from docx import Document
import os, json

def read_questions_answers(filename):
    """Liest eine .docx-Datei und legt ein dictionary mit Frage/Antwort Paaren 
    an Voraussetzung: Fragen enden mit einem '?' es folgt ein Zeilenumbruch und 
    ein Anwortblock"""
    doc = Document(filename)
    qa_dict = {}
    current_question = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if text.endswith("?"):
            # Es ist eine Frage
            current_question = text
            qa_dict[current_question] = ""
        elif current_question:
            # Es ist eine Antwort zu der zuletzt gefundenen Frage
            qa_dict[current_question] += text + "\n"

    # Entferne den letzten Zeilenumbruch von jeder Antwort
    for question in qa_dict:
        qa_dict[question] = qa_dict[question].strip()

    return qa_dict

def write_qa_dictionary(folder_path='data/'):
    """Liest alle docx-Dateien im Data-Folder und gibt sie als Frage/Anwort Paare
    in einem dictionary zurück"""
    qa_dict = {}
    # Iteration über alle Dateien in folder_path
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            current_file = read_questions_answers(file_path)
            qa_dict.update(current_file)
    return qa_dict

def make_json(dict,folder_path='',file_name='data.json'):
    """Erhält ein Dictionary als Parameter und gibt eine .json Datei aus"""
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as outfile:
        json.dump(dict, outfile, indent=4)

def update_json(question, folder_path='', file_name='progress.json'):
    """Aktualisiert die JSON-Datei, indem der Zähler für die gegebene Frage erhöht wird"""
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as infile:
            try:
                existing_data = json.load(infile)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    return existing_data.get(question, 0) >= 3

# Uncomment to generate new data.json
# make_json(write_qa_dictionary())