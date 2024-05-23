import json
import requests
import re
import random
import os

HOST = str(os.getenv("HOST"))

URL = "http://" + HOST + "/v1/chat/completions"
HEADERS = {
    'Content-Type': 'application/json',
    'accept': 'application/json'
}

def create_request(prompt):

    # encode json

    request = {
        "model": "string",
        "messages": [
          {
            "role": "user",
            "content": prompt
          }
        ],
        "tools": [],
        "do_sample": True,
        "temperature": 0,
        "top_p": 0,
        "n": 1,
        "max_tokens": 64,
        "stream": False
    }

    return request

def split(distractor_string):

    pattern = fr'<false>(.*?)</false>'
    matches = re.findall(pattern, distractor_string)

    distractors = [match.strip() for match in matches]

    print(distractor_string)

    return distractors


def fetch_and_split(prompt):
    request_json = create_request(prompt)
    response = requests.post(URL, headers=HEADERS, json=request_json)

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return []

    content = response.json()["choices"][0]["message"]["content"]
    return split(content)

def setup(database, dataset, num_distractors):

    for dp in dataset:
        if database.check_database(dp["question"]):
            continue

        base_prompt = (
            "<context> " + dp["context"] + " </context>\n"
            + "<question> " + dp["question"] + " </question>\n"
            + "<true> " + dp["correct"] + " </true>\n"
        )

        distractors = []
        retries = 0
        while len(distractors) < num_distractors and retries < 8:
            random.shuffle(distractors)
            current_prompt = base_prompt + "".join(["<false> " + distractor + " </false>\n" for distractor in distractors])
            new_distractors = fetch_and_split(current_prompt)
            retries += 1
            for new_distractor in new_distractors:
                if new_distractor == "" or (new_distractor in distractors) or new_distractor == dp["correct"]:
                    continue

                distractors.append(new_distractor)
                if len(distractors) == num_distractors:
                    break

        yield dp["context"], dp["question"], dp["correct"], distractors
