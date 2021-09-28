# Rasa NLU training data / domain generator with Parrot paraphrasing

## Purpose

This is a simple training data generator for Rasa framework, which can be used to speed-up your dev cycle a bit by enriching [NLU training data](https://rasa.com/docs/rasa/nlu-training-data) / [domain](https://rasa.com/docs/rasa/domain) files with additional samples, generated with [Parrot](https://pythonrepo.com/repo/PrithivirajDamodaran-Parrot-python-natural-language-processing).

The input to generator is a CSV file (by default in `./data/input/sample_intents.csv`), which contains single original intent example (column `intent_orignal_phrase`) and single original response (column `intent_original_response`).

The output is a set of two files, which includes original intent / response and their paraphrased alternatives:
* `./output/nlu.yml` with NLU training data
* `./output/domain.yml` with domain data

Output files are built based on templates under `./data/templates`.

## Sample usage

For example, let's say we have the following original intent defined in `./data/inputs/sample_intents.csv`:
* intent_orignal_phrase: When is your vacation?
* intent_original_response: I'm planning for New Zealand some time next year.

If needed, check and update input /ouput config in `.env`. Otherwise you can simply use default paths.

Install dependencies and run `generate.py` to enrich training data: 
```
pip3 install -r requirements.txt
python3 generate.py
```

Here is a sample generated intent in NLU data:
```
- intent: 027a948b20ff4592b97e31dc87d0bc97
  examples: |
    - When is your vacation?
    - when do you take a holiday?
    - when do you take a break?
    - when do you take a vacation?
    - when is your holiday?
    - when are your vacations?
    - when's your vacation?
    - when is your vacation?
```

And here is the generated domain section for the same intent:
```
  utter_027a948b20ff4592b97e31dc87d0bc97:
  - text: I'm planning for New Zealand some time next year.
  - text: next year i'm planning a trip to new zealand
  - text: next year i'm planning to visit new zealand
  - text: next year i'm planning to go to new zealand
  - text: next year i'm planning on visiting new zealand
  - text: next year i'm planning on going to new zealand
  - text: i plan to go to new zealand next year
  - text: i plan to visit new zealand sometime next year
  - text: i plan to go to new zealand sometime next year
  - text: i'm planning to go to new zealand sometime next year
  - text: i'm planning to visit new zealand sometime next year
```
