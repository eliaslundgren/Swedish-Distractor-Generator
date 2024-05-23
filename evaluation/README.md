## Usage

```bash
python evaluate.py
```

The terminal will be used as user interface, for the interface to fit at least 10 lines are required - resize your terminal accordingly.

## Instructions

Your task is to select good quality distractors (incorrect alternatives) for multiple choice questions. You will be shown a question, the correct answer and a list of four distractors.

Distractors are marked using their corresponding number key. This key, along with a checkbox will be displayed next to each distractor. A distractor is marked as correct if the checkbox is checked. You can select as many distractors as you like, or none at all. When you are ready to submit your rating and proceed to next question press the enter or space key. If you need to exit the program, press ESC, your progress will be saved.

To avoid bias - do not look at evaluation.json before rating.

### Rating instructions

- Each distractor should be rated from the perspective that you don't know the answer to the question.
- Focus on the distractor's grammar, relevance, and how well it fits the question.
- If the distractor is, or is similar to the correct answer, it should be rated as incorrect.
- If the same distractor is shown multiple times for one question, rate them all the same way, as if they were unrelated.

## When you're done

When you're done, thank you! Please send the results.db file to:

```email
elias.lundgren00@gmail.com
```
