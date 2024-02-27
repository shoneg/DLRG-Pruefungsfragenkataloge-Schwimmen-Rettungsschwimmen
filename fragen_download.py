import argparse
import requests
import json
import re

Alle_Arten = [
    (1, 'Juniorretter', 'J'),
    (2, 'Deutsches_Rettungsschwimmabzeichen_Bronze', 'DRSAB'),
    (3, 'Deutsches_Rettungsschwimmabzeichen_Silber', 'DRSAS'),
    (4, 'Deutsches_Rettungsschwimmabzeichen_Gold', 'DRSAG'),
    (5, 'Lehrscheininhaber', 'L'),
    (8, 'Deutsches_Schnorcheltauchabzeichen', 'DSTA'),
    (10, 'Ausbilder_Schwimmen', 'AS'),
    (11, 'Ausbilder_Rettungsschwimmen', 'ARS'),
    (12, 'Ausbildungsassistent_Schwimmen', 'AAS'),
    (13, 'Ausbildungsassistent_Rettungsschwimmen', 'AARS')
]

def get_url():
    url = "https://www.dlrg.de/informieren/ausbildung/pruefungsfragenquiz/"
    response = requests.get(url)
    if response.status_code == 200:
        # Find the URL value using regular expressions
        pattern = re.compile(r'var\s+url\s*=\s*"([^"]+)"')
        match = pattern.search(response.content.decode())
        if match:
            return match.group(1)
        else:
            return None
    else:
        print("Error:", response.status_code)
        return None

def parse_jsonp(jsonp):
    # Finde die Position der ersten öffnenden Klammer
    start_index = jsonp.find("(")
    # Finde die Position der letzten schließenden Klammer
    end_index = jsonp.rfind(")")
    # Extrahiere den JSON-Teil
    json_str = jsonp[start_index + 1:end_index]
    # Analysiere den JSON-Teil
    return json.loads(json_str)

def get_questions(idx=None):
    response = requests.get(get_url() + '&callback=?', params={'quizSelection': idx})
    retVal = parse_jsonp(response.text)
    quiz = retVal
    if 'error' in quiz and quiz['error'] == 'forbidden':
        print('error')
    quiz['fragenPointer'] = 0
    return quiz

def extract_questions(json_data):
    questions = {}
    for frage_id, frage_info in json_data["fragen"].items():
        if frage_id not in questions:
            questions[frage_id] = {
                "id": frage_info["id"],
                "frage": frage_info["frage"],
                "antworten": frage_info["antworten"],
                "kapitel": frage_info["kapitel"],
                "kapitelBez": frage_info["kapitelBez"],
            }
    return questions

def main(wiederholungen, pfad, kataloge, alle_schreiben = False):
    fragen = {art[1]: {} for art in kataloge}
    fragen['Alle'] = {}
    for art_idx, art_str, _ in kataloge:
        for _ in range(wiederholungen):
            neue_fragen = extract_questions(get_questions(art_idx))
            fragen[art_str].update(neue_fragen)
            fragen['Alle'].update(fragen[art_str])
    
    for art in fragen.keys():
        if art == 'Alle' and not alle_schreiben:
            continue
        with open(f'{pfad}/{art}.json', 'w') as fragen_datei:
            sortierte_fragen = dict(sorted(fragen[art].items(), key=lambda x: int(x[0])))
            json.dump(sortierte_fragen, fragen_datei, indent=2, ensure_ascii=False)
        
    keys = [int(k) for k in fragen['Alle'].keys()]
    keys.sort()
    print(f'Es wurden {len(keys)} Fragen mit den folgenden IDs gefunden:')
    print(keys)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DLRG Fragen abrufen und speichern', epilog='KATALOGE=\n' + '\n'.join([f"{art[1]} ({art[2]})" for art in Alle_Arten]), formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-w', '--wiederholungen', type=int, default=100, help='Anzahl der Wiederholungen (Standard: 100)')
    parser.add_argument('-p', '--pfad', type=str, default='fragen', help='Speicherpfad für Dateien (Standard: ./fragen)')
    parser.add_argument('-k', '--kataloge', nargs='+', default=['Alle'], choices=[art[1] for art in Alle_Arten],
                        help='Fragenkataloge auswählen (Standard: Alle)', metavar='KATALOG')
    
    args = parser.parse_args()
    
    if args.kataloge == ['Alle']:
        main(args.wiederholungen, args.pfad, Alle_Arten, True)
    else:
        chosen_kataloge = []
        for art in Alle_Arten:
            if art[1] in args.kataloge or art[2] in args.kataloge:
                chosen_kataloge.append(art)
        main(args.wiederholungen, args.pfad, chosen_kataloge)
        