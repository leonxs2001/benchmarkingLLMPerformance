import csv
import os
import time
import datetime
import random
import google.generativeai as genai
from openai import OpenAI

from secret_settings import CHAT_GPT_API_KEY, GEMINI_API_KEY

SOURCE_FILE_PROMPT = "Geben Sie den Pfad zu der Datei mit den Fragen für die LLMs an. Es sollten mindestends 20 Fragen enthalten sein. Bei keiner Angabe wird die Datei requestpool aus dem assets Ordner aufgerufen."
DESTINATION_DIRECTORY_PROMPT = "Geben Sie den Pfad zu dem Ordner an, in welchem die Ergebniss gespeichert werden sollen. Bei keiner Angabe wird der Ordner der Ausführung verwendet."
PYTHON_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
SOURCE_CSV_FILE_PATH = PYTHON_FILE_PATH + "\\assets\\requestpool.csv"
CHAT_GPT_MODEL = "gpt-3.5-turbo-0125"
GEMINI_MODEL = "gemini-pro"

chat_gpt_client = OpenAI(
    api_key=CHAT_GPT_API_KEY,
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
            result_list.append((prompt[0], benchmark_for_chat_gpt_pro_1_0(prompt[1]), benchmark_for_gemini(prompt[1])))

        write_result_list_in_csv_file(destination_path, result_list)


def benchmark_for_chat_gpt_pro_1_0(prompt):
    print("Benchmark start chat gpt")
    start_time = time.time()
    completion = chat_gpt_client.chat.completions.create(
        model=CHAT_GPT_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    end_time = time.time()
    print("Benchmark end chat gpt")
    return len(completion.choices[0].message.content), end_time - start_time


def benchmark_for_gemini(prompt):
    print("Benchmark start gemini")
    start_time = time.time()
    response_gemini = gemini_model.generate_content(prompt)
    end_time = time.time()
    print("Benchmark end gemini")
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
            ["Prompt Id", "ChatGPT Anzahl Zeichen", "ChatGPT responsetime in Sekunden",
             "ChatGPT Responsegeschwindigkeit in Zeichen/Sekunden", "Gemini Anzahl Zeichen",
             "Gemini responsetime in seconds", "Gemini Responsegeschwindigkeit in Zeichen/Sekunden"])

        print("starts writing information's")
        for result in result_list:
            prompt = result[0]
            chat_gpt_number_of_chars = result[1][0]
            chat_gpt_response_time = result[1][1]
            chat_gpt_response_speed = get_response_speed(chat_gpt_number_of_chars, chat_gpt_response_time)

            gemini_number_of_chars = result[2][0]
            gemini_response_time = result[2][1]
            gemini_response_speed = get_response_speed(gemini_number_of_chars, gemini_response_time)
            print("start writing dataset")
            csv_writer.writerow([prompt, chat_gpt_number_of_chars, chat_gpt_response_time, chat_gpt_response_speed,
                                 gemini_number_of_chars, gemini_response_time, gemini_response_speed])
            print("end writing dataset")


def get_response_speed(number_of_chars, response_time):
    return number_of_chars / response_time


if __name__ == '__main__':
    start_benchmark_performance_llm()
