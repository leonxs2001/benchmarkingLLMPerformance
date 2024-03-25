import csv
import os


def start_benchmark_performance_llm():
    path = input("Geben Sie den Pfad zu der Datei mit den Fragen für die LLMs an. Es sollten mindestends 20 Fragen enthalten sein. Bei keiner Angabe wird die Datei requestpool aus dem assets Ordner aufgerufen.")
    if not path:
        path = os.path.dirname(os.path.abspath(__file__)) + "\\assets\\requestpool.csv"
        print(path)
    print(get_questions_from_csv(path))

def get_questions_from_csv(path):
    with open(path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)

        questions = []

        for row in csv_reader:
            questions.append(row[0])

        return questions


if __name__ == '__main__':
    start_benchmark_performance_llm()
