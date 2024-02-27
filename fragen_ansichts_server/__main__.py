import argparse
from flask import Flask, render_template, request
import json
import os
from typing import List, Dict, Union

app = Flask(__name__)

# Pfad zu deinem JSON-Ordner
json_folder_path: str = './fragen'


def merge_json_files(folder_path: str) -> List[Dict[str, Union[str, Dict[str, Union[int, str, List[str]]]]]]:
    json_files: List[Dict[str, Union[str, Dict[str, Union[int, str, List[str]]]]]] = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            with open(os.path.join(folder_path, file_name)) as f:
                json_data = json.load(f)
                for key, value in json_data.items():
                    if isinstance(value, dict) and 'id' in value:
                        value['datei'] = file_name[:-5]  # Entfernen der ".json"-Endung
                        json_files.append(value)
    return json_files

def make_dicts_distinct(outer_list, attribute):
    distinct_dicts = []
    seen_values = set()

    for inner_dict in outer_list:
        attr_value = inner_dict.get(attribute)
        if attr_value not in seen_values:
            distinct_dicts.append(inner_dict)
            seen_values.add(attr_value)

    return distinct_dicts


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    # Laden und Zusammenführen aller JSON-Dateien
    json_files = merge_json_files(json_folder_path)

    # Eindeutige Werte für Datei und Kapitel extrahieren
    unique_files = sorted(set(json_data.get('datei', '') for json_data in json_files))
    unique_files.remove('Alle')
    unique_chapters = sorted(set(json_data.get('kapitelBez', '') for json_data in json_files))

    # Standardwerte für Filter
    selected_file = 'Alle'
    selected_chapter = ''
    show_question = True
    show_answer = True
    show_category = True

    # Wenn ein Filter angewendet wird
    if request.method == 'POST':
        selected_file = request.form.get('file', 'Alle')
        selected_chapter = request.form.get('chapter', '')
        show_question = request.form.get('show_question', '') == 'true'
        show_answer = request.form.get('show_answer', '') == 'true'
        show_category = request.form.get('show_category', '') == 'true'

    # Kapitel, die in der ausgewählten Datei vorkommen
    file_chapters = set()
    if selected_file != 'Alle':
        for json_data in json_files:
            if selected_file == json_data.get('datei'):
                file_chapters.add(json_data.get('kapitelBez', ''))
                
    # Filtern der Fragen basierend auf den ausgewählten Kriterien
    filtered_questions: List[Dict[str, Union[int, str, List[str]]]] = []
    for json_data in json_files:
        if selected_file == 'Alle' or selected_file == json_data.get('datei'):
            if selected_chapter == '' or selected_chapter == json_data.get('kapitelBez'):
                filtered_question = {}
                filtered_question['id'] = json_data.get('id')
                if show_question:
                    filtered_question['frage'] = json_data.get('frage')
                if show_answer:
                    filtered_question['antworten'] = json_data.get('antworten')
                if show_category:
                    filtered_question['kapitel'] = json_data.get('kapitel')
                    filtered_question['kapitelBez'] = json_data.get('kapitelBez')
                filtered_questions.append(filtered_question)
                
    filtered_questions = make_dicts_distinct(filtered_questions, 'id')

    return render_template('index.html', json_files=json_files, filtered_questions=filtered_questions,
                           unique_files=unique_files, unique_chapters=unique_chapters,
                           selected_file=selected_file, selected_chapter=selected_chapter,
                           show_question=show_question, show_answer=show_answer, show_category=show_category,
                           file_chapters=file_chapters)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DLRG Fragen auf einer Website anzeigen', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-p', '--port', type=int, default=5000, help='Port, auf dem der Server lauscht. (Standard: 5000)')
    parser.add_argument('-f', '--fragen', type=str, default='./fragen', help='Speicherpfad zum Ordner, der die Dateien mit den anzuzeigenden Fragen hat. Die Fragen sollten mit dem Skript fragen_download.py heruntergeladen worden sein. (Standard: ./fragen)')
    args = parser.parse_args()
    json_folder_path = args.fragen
    app.run(debug=True, port=args.port)
