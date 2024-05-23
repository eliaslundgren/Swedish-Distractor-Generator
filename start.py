
from rating import Rating
from database import Database
from autorating import AutoRating
from api import setup as api_setup

import argparse
import curses
import numpy as np
import json
import re

def get_tag(tag, input):
    pattern = fr'<{tag}>(.*?)</{tag}>'
    pattern = re.compile(pattern, re.DOTALL)
    matches = re.findall(pattern, input.strip())
    return [match.strip() for match in matches]

def extract(dataset_path):
    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    extracted = []

    for dp in dataset:
        instruction = dp["instruction"]
        output = dp["output"]
        extracted.append({
            "context": get_tag("context", instruction)[0],
            "question": get_tag("question", instruction)[0],
            "correct": get_tag("true", instruction)[0],
            "distractors": get_tag("false", output)
        })

    return extracted


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-db', '--database', type=str, required=True, help="Database to save ratings")
    parser.add_argument('-r', '--rater', type=str, required=True, help="How to rate the generated distractors")
    args = parser.parse_args()

    # based on model we want a generator class that we can call generate on

    database = Database(args.database)
    rating = Rating(database) if args.rater == "manual" else AutoRating(database)


    JSON_DATASET = "data/swe_mcq_train.json"
    DATASET = extract(JSON_DATASET)
    NUM_DISTRACTORS = 4
    START_SEED = 0
    seed = START_SEED

    generator = api_setup(database, DATASET, NUM_DISTRACTORS)

    if args.rater == "manual":

        def run(scr):
            for values in generator:
                success = rating.rate(*values)
                if not success:
                    return
        curses.wrapper(run)
    else:
        for values in generator:
            success = rating.rate(*values)
            if not success:
                break



    # gets the next context, question, answer, distractors and sends to rating env


    print("Exiting...")
