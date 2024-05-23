# Mistral 7B Swedish Distractor Generator

This repo contains the code and data used for training, creating preference data and evaluating the Swedish distractor generator introduced in the my master thesis [Available Here Later](). More details about the components of this repo can be found in the thesis.

## Setup

This implementation does not run the model locally. Instead it expects an API to be running on some host, defined by the environment variable `HOST`. The API should follow an OpenAI-style API specification. The thesis implementation relied on [LLaMa-Factory](https://github.com/hiyouga/LLaMA-Factory) to train and host the model.

If you wish to use the automatic GPT-4 based distractor rating you need to specify the `OPENAI_API_KEY` in the environment.

## Usage

The main script for creating preference ratings is `start.py`. It has two arguments which are required:

- `--database | --db` The database where the ratings should be saved
- `--rater | --r` The method of rating. Either `manual` or `auto`

```bash
python start.py --db <database> --r <rating method>
```

### Database

To view a created database you can use the `database.py` script. It takes the database as an argument.

```bash
python database.py --db <database>
```

### Evaluation

The scripts used for human evaluation of the final model can be found in the `evaluation` folder. The instruction for the evaluators is available in the README in that folder, and the script for running the evaluation is `evaluation.py`.

```bash
python evaluation.py
```

## Model

The final model is available on [Huggingface]()

## Data

In the `data` folder you can find the data used for supervised, fine-tuning, direct preference optimization and evaluation. The data is and extended version of the data used in [SweQUAD-MC](https://github.com/dkalpakchi/SweQUAD-MC)
