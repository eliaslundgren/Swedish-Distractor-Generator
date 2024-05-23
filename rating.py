import curses
import random
import textwrap


class Rating:
    def __init__(self, db):
        stdscr = curses.initscr()
        stdscr.clear()
        curses.curs_set(0)
        curses.noecho()
        self.scr = stdscr

        self.db = db

    def rate(self, context, question, answer, distractors):

        # if already rated
        if self.db.check_database(question):
            return True

        options = [*distractors, answer]
        random.shuffle(options)
        selections = [False] * len(options)

        while True:
            self.scr.clear()

            height, width = self.scr.getmaxyx()

            self.scr.addstr(0, 0, "Context:")
            # Wrap text to fit the window width
            n = 1
            wrapped_text = textwrap.wrap(context, int(width * 0.9))
            for i, line in enumerate(wrapped_text):
                print(line)
                self.scr.addstr(n, 0, line)
                n += 1
                if i > 4:
                    break

            self.scr.addstr(n + 1, 0, "Question:")
            self.scr.addstr(n + 2, 0, question)
            n += 4
            for i, option in enumerate(options):
                checkbox = "[x]" if selections[i] else "[ ]"
                self.scr.addstr(i + n, 0, f"{i + 1}. {checkbox} {option}")

            self.scr.refresh()

            # Handle input
            key = self.scr.getch()
            if key in [27, curses.KEY_EXIT]:
                self.scr.clear()
                self.scr.refresh()
                return False
            elif key in [10, 13, 32, curses.KEY_ENTER]:
                break
            elif 0 < key - 48 <= len(options):
                selections[key - 49] = not selections[key - 49]

        # clear and save - await for next
        self.scr.clear()
        self.scr.refresh()

        context_id = self.db.save_context(context, question, answer)
        for i, option in enumerate(options):
            if option == answer:
                continue
            self.db.save_distractor(context_id, option, selections[i])

        return True

    def close(self):
        curses.endwin()
