import sys
import json
import sqlite3
import curses
import random

OUT_DB = "results.db"
SRC_JSON = "evaluation.json"

class Evaluate:
    def __init__(self):
        with open(SRC_JSON, "r") as f:
            self.dataset = json.load(f)

        self.setup_database()
        self.index = self.load_database()
        if self.index is None:
            print("Database is full")
            sys.exit(1)

        print("loaded", self.index)

    def setup_database(self):
        self.connection = sqlite3.connect(OUT_DB)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS results (
                                context TEXT NOT NULL,
                                question TEXT NOT NULL,
                                distractor TEXT NOT NULL,
                                source TEXT NOT NULL,
                                accepted INTEGER NOT NULL)''')
        self.connection.commit()

    def check_database(self, question):
        query = "SELECT * FROM results WHERE question = ?"
        self.cursor.execute(query, (question,))
        result = self.cursor.fetchone()
        return result is not None

    def load_database(self):
        # find the next index to show the user in the database
        # if database is full, return None
        for index, datapoint in enumerate(self.dataset):
            if not self.check_database(datapoint["question"]):
                return index

    def save_current(self, selection):
        if self.index is None:
            return

        data = self.dataset[self.index]
        for i, distractor in enumerate(data["distractors"]):
            self.cursor.execute("INSERT INTO results (context, question, distractor, source, accepted) VALUES (?, ?, ?, ?, ?)",
                                (data["context"], data["question"], distractor, data["sources"][i], selection[i]))
        self.connection.commit()

        self.index += 1
        if self.index >= len(self.dataset):
            self.index = None

    def run(self, scr):

        print("running")

        while self.index is not None:
            data = self.dataset[self.index]
            distractors = data["distractors"]
            sources = data["sources"]

            selection = [False] * len(distractors)

            while True:
                scr.clear()

                scr.addstr(0, 0,"Select good distractors using the NUMBER keys. Press ENTER / SPACE to submit. Press ESC to exit." + " (" + str(self.index + 1)+ "/" + str(len(self.dataset)) + ")")
                scr.addstr(2, 0, "Question: " + data["question"])
                scr.addstr(3, 0, "Answer: " + data["answer"])
                for i, option in enumerate(distractors):
                    checkbox = "[x]" if selection[i] else "[ ]"
                    scr.addstr(i + 5, 0, f"{i + 1}. {checkbox} {option}")

                scr.refresh()

                # Handle input
                key = scr.getch()
                if key in [27, curses.KEY_EXIT]:
                    scr.clear()
                    scr.refresh()
                    return
                elif key in [10, 13, 32, curses.KEY_ENTER]:
                    self.save_current(selection)
                    break
                elif 0 < key - 48 <= len(distractors):
                    selection[key - 49] = not selection[key - 49]


if __name__ == "__main__":
    def start(scr):
        scr.clear()
        curses.curs_set(0)
        curses.noecho()
        evaluator = Evaluate()
        evaluator.run(scr)

    curses.wrapper(start)
