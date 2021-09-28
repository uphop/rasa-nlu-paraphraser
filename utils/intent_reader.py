import uuid
import logging
logging.basicConfig(level=logging.DEBUG)
from csv import DictReader
import os

class IntentReader:
    def __init__(self):
        # get input / ouput details from config
        self.INPUT_FILE_NAME = os.getenv('INPUT_FILE_NAME', './data/input/sample_intents.csv')

    def read_intents(self):
        intents = []
        with open(self.INPUT_FILE_NAME, 'r') as read_obj: 
            csv_dict_reader = DictReader(read_obj)
            for row in csv_dict_reader:
                intent = row
                intent['intent_name'] = str(uuid.uuid4().hex)
                intents.append(intent)
        return intents