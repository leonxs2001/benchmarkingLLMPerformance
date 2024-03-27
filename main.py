import csv
import os
import time
import datetime
import random

SOURCE_FILE_PROMPT = "Geben Sie den Pfad zu der Datei mit den Fragen für die LLMs an. Es sollten mindestends 20 Fragen enthalten sein. Bei keiner Angabe wird die Datei requestpool aus dem assets Ordner aufgerufen."
DESTINATION_DIRECTORY_PROMPT = "Geben Sie den Pfad zu dem Ordner an, in welchem die Ergebniss gespeichert werden sollen. Bei keiner Angabe wird der Ordner der Ausführung verwendet."
PYTHON_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
SOURCE_CSV_FILE_PATH = PYTHON_FILE_PATH + "\\assets\\requestpool.csv"


def start_benchmark_performance_llm(number_of_iterations=3):
    source_path = input(SOURCE_FILE_PROMPT)
    if not source_path:
        source_path = SOURCE_CSV_FILE_PATH

    destination_path = input(DESTINATION_DIRECTORY_PROMPT)
    if not destination_path:
        destination_path = PYTHON_FILE_PATH

    questions = get_questions_from_csv(source_path)

    for i in range(3):
        result_list = list()

        for question in questions:
            result_list.append((question, benchmark_for_chat_gpt_pro_1_0(question), benchmark_for_gemini_3_5(question)))

        write_result_list_in_csv_file(destination_path, result_list)


def benchmark_for_chat_gpt_pro_1_0(question):
    start_time = time.time()
    result = ask_chat_gpt_pro_1_0(question)
    end_time = time.time()
    return len(result), end_time - start_time


def ask_chat_gpt_pro_1_0(question):
    # TODO add code
    return question


def benchmark_for_gemini_3_5(question):
    start_time = time.time()
    result = ask_gemini_3_5(question)
    end_time = time.time()
    return len(result), end_time - start_time


def ask_gemini_3_5(question):
    # TODO add code
    return question


def get_questions_from_csv(path, number_of_questions=20):
    with open(path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter="|")

        questions = []

        for row in csv_reader:
            questions.append(row[0])

        return random.sample(questions, number_of_questions)


def write_result_list_in_csv_file(path, result_list):
    i = 0
    result_path = os.path.join(path, datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S_%f") + "_" + str(i) + ".csv")
    while os.path.isfile(result_path):
        result_path = os.path.join(path, datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S_%f") + "_" + str(i) + ".csv")

    with open(result_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerow(["Fragen", "ChatGPT Anzahl Zeichen", "ChatGPT responsetime in seconds", "Gemini Anzahl Zeichen",
                             "Gemini responsetime in seconds"])
        for result in result_list:
            csv_writer.writerow([result[0], result[1][0], result[1][1], result[2][0], result[2][1]])


if __name__ == '__main__':
    start_benchmark_performance_llm()
