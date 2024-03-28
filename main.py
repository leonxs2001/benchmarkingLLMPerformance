import csv
import os
import time
import datetime
import random
import google.generativeai as genai
from openai import OpenAI

from secret_settings import GPT_API_KEY, GEMINI_API_KEY

SOURCE_FILE_PROMPT = "Geben Sie den Pfad zu der Datei mit den Fragen für die LLMs an. Es sollten mindestends 20 Fragen enthalten sein. Bei keiner Angabe wird die Datei requestpool aus dem assets Ordner aufgerufen."
DESTINATION_DIRECTORY_PROMPT = "Geben Sie den Pfad zu dem Ordner an, in welchem die Ergebniss gespeichert werden sollen. Bei keiner Angabe wird der Ordner der Ausführung verwendet."
PYTHON_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
SOURCE_CSV_FILE_PATH = PYTHON_FILE_PATH + "\\assets\\requestpool.csv"
GPT_MODEL = "gpt-3.5-turbo-0125"
GEMINI_MODEL = "gemini-pro"

gpt_client = OpenAI(
    api_key=GPT_API_KEY,
)

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(GEMINI_MODEL)


def start_benchmark_performance_llm(number_of_iterations=3):
    source_path = input(SOURCE_FILE_PROMPT)
    if not source_path:
        source_path = SOURCE_CSV_FILE_PATH

    destination_path = input(DESTINATION_DIRECTORY_PROMPT)
    if not destination_path:
        destination_path = PYTHON_FILE_PATH

    for i in range(number_of_iterations):
        print(f"{i}st Iteration.")
        prompts = get_prompts_from_csv(source_path)
        result_list = list()

        for prompt in prompts:
            result_list.append((prompt[0], benchmark_for_gpt_pro_3_5(prompt[1]), benchmark_for_gemini_pro(prompt[1])))

        write_result_list_in_csv_file(destination_path, result_list)


def benchmark_for_gpt_pro_3_5(prompt):
    print("Benchmark start gpt-3.5")
    start_time = time.time()
    completion = gpt_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    end_time = time.time()
    print("Benchmark end gpt-3.5")
    return len(completion.choices[0].message.content), end_time - start_time


def benchmark_for_gemini_pro(prompt):
    print("Benchmark start gemini pro")
    start_time = time.time()
    response_gemini = gemini_model.generate_content(prompt)
    end_time = time.time()
    print("Benchmark end gemini pro")
    return len(response_gemini.candidates[0].content.parts[0].text), end_time - start_time


def get_prompts_from_csv(path, number_of_prompts=20):
    with open(path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=";")

        prompts = []

        for row in csv_reader:
            prompts.append((row[0], row[1]))

        return random.sample(prompts, number_of_prompts)


def write_result_list_in_csv_file(path, result_list):
    result_path = os.path.join(path, datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S_%f") + ".csv")
    with open(result_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerow(
            ["Prompt Id", "GPT-3.5 Anzahl Zeichen", "GPT-3.5 responsetime in Sekunden",
             "GPT-3.5 Responsegeschwindigkeit in Zeichen/Sekunden", "Gemini Pro Anzahl Zeichen",
             "Gemini Pro responsetime in seconds", "Gemini Pro Responsegeschwindigkeit in Zeichen/Sekunden"])

        print("starts writing information's")
        for result in result_list:
            prompt = result[0]
            gpt_number_of_chars = result[1][0]
            gpt_response_time = result[1][1]
            gpt_response_speed = get_response_speed(gpt_number_of_chars, gpt_response_time)

            gemini_number_of_chars = result[2][0]
            gemini_response_time = result[2][1]
            gemini_response_speed = get_response_speed(gemini_number_of_chars, gemini_response_time)
            print("start writing dataset")
            csv_writer.writerow([prompt, gpt_number_of_chars, gpt_response_time, gpt_response_speed,
                                 gemini_number_of_chars, gemini_response_time, gemini_response_speed])
            print("end writing dataset")


def get_response_speed(number_of_chars, response_time):
    return number_of_chars / response_time


if __name__ == '__main__':
    start_benchmark_performance_llm()
