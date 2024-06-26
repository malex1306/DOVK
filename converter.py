from docx import Document
import os, json

def read_questions_answers(filename):
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
    qa_dict = {}
    # Iteration über alle Dateien in folder_path
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            current_file = read_questions_answers(file_path)
            qa_dict.update(current_file)
    return qa_dict

def make_json(dict,folder_path='',file_name='data.json'):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as outfile:
        json.dump(dict, outfile, indent=4)

# Uncomment to generate new data.json
make_json(write_qa_dictionary())