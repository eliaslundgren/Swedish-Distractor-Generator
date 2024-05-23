import sqlite3
import curses
import sys

class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def view(self, scr):
        stdscr = scr
        stdscr.clear()
        curses.curs_set(0)
        curses.noecho()

        self.cursor.execute('''SELECT * FROM context''')
        contexts = self.cursor.fetchall()
        if len(contexts) == 0:
            curses.curs_set(1)
            curses.endwin()
            return
        current = 0


        def update():
            n, c, q, a = contexts[current]
            self.cursor.execute('''SELECT * FROM distractor WHERE context_id = (?)''', [str(n)], )
            ds = self.cursor.fetchall()
            d = []
            s = []
            for dp in ds:
                dl = list(dp)
                d.append(dl[2])
                s.append(dl[3])
            return q, a, d, s

        question, answer, distractors, selections = update()

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, question)
            stdscr.addstr(2, 0, "1. [a] " + answer)

            for i, distractor in enumerate(distractors):
                checkbox = "[x]" if selections[i] else "[ ]"
                stdscr.addstr(i + 3, 0, f"{i + 2}. {checkbox} {distractor}")

            stdscr.refresh()

            # Handle input
            key = stdscr.getch()
            if key in [10, 13, 32, curses.KEY_ENTER]:
                current += 1
                if current >= len(contexts):
                    curses.curs_set(1)
                    curses.endwin()
                    return
                question, answer, distractors, selections = update()

    def setup_database(self):
        # Context Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS context (
                              context_id INTEGER PRIMARY KEY,
                              context TEXT NOT NULL,
                              question TEXT NOT NULL,
                              answer TEXT NOT NULL)''')
        # Distractor Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS distractor (
                              option_id INTEGER PRIMARY KEY,
                              context_id INTEGER NOT NULL,
                              distractor TEXT NOT NULL,
                              accepted INTEGER NOT NULL,
                              FOREIGN KEY(context_id) REFERENCES questions(context_id))''')

        self.conn.commit()

    def check_database(self, question):
        query = "SELECT * FROM context WHERE question = ?"
        self.cursor.execute(query, (question,))
        result = self.cursor.fetchone()
        return result is not None

    def save_context(self, context, question, answer):
        insert_query = '''INSERT INTO context (context, question, answer) VALUES (?, ?, ?)'''
        self.cursor.execute(insert_query, (context, question, answer))
        self.conn.commit()
        return self.cursor.lastrowid  # Returns the ID of the newly inserted row

    def save_distractor(self, context_id, distractor, accepted):
        insert_query = '''INSERT INTO distractor (context_id, distractor, accepted) VALUES (?, ?, ?)'''
        self.cursor.execute(insert_query, (context_id, distractor, accepted))
        self.conn.commit()
        return self.cursor.lastrowid  # Returns the ID of the newly inserted row





if __name__ == '__main__':
    db = sys.argv[1:][0]
    if not db:
        print("Usage: python database.py <database>")
        sys.exit(1)

    def view(scr):
        database = Database(db)
        database.view(scr)

    curses.wrapper(view)
