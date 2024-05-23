import json
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

with open('prompt.txt', 'r') as file:
    PROMPT = file.read()

# Hitta bättre prompt som bättre definierar vad ett poäng betyder, upprepa med 1-5 kan va dålig
# Skicka contextet på frågan

def build_prompt(context, question, answer, distractors):
    distractors_text = "".join([f"\n[DISTRACTOR {i + 1}] {distractor}" for i, distractor in enumerate(distractors)])
    return "[QUESTION] " + question + "\n[ANSWER] " + answer + distractors_text


class AutoRating:

    def __init__(self, db):
        self.db = db

    def rate_via_api(self, user_prompt):
        retries = 0
        while retries < 3:
            try:
                completion = client.chat.completions.create(
                    model= "gpt-4-0125-preview",
                    messages=[
                        {"role": "system",
                         "content": PROMPT},
                        {"role": "user",
                         "content": user_prompt}
                    ]
                )

                return completion.choices[0].message.content
            except Exception as e:
                retries += 1
                print(f"An error occurred: {e}. Waiting 10 seconds and trying again.")
                time.sleep(10)
        raise Exception("Failed to get a response from OpenAI after 3 attempts.")

    def rate(self, context, question, answer, distractors):
        if self.db.check_database(question):
            return True

        if len(distractors) == 0:
            print("Skip")
            return True

        prompt = build_prompt(context, question, answer, distractors)

        print("GPT PROMPT:", prompt)

        while True:
            try:
                result = self.rate_via_api(prompt)
                print("GPT RESULT:", result)
                result = result.split("$")[1]
                scores = json.loads(result)
                if len(scores) == len(distractors):
                    break
            except Exception:
                pass


        print("\n",question,answer,"\n")
        for i, distractor in enumerate(distractors):
            print(distractor, scores[i])
        print("")
        context_id = self.db.save_context(context, question, answer)

        # Captures more data
        # This is still preference, so even two bad datapoints might give some good data
        avg = sum(scores) / len(scores)
        mid = 2.5
        dif = avg - mid
        limit = mid + dif*0.5

        for i, distractor in enumerate(distractors):

            self.db.save_distractor(context_id, distractor, scores[i] > limit)

        return True

    def close(self):
        pass
