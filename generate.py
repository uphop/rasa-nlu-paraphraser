from csv import DictReader
from generators.nlu_generator import NLUEGenerator
from generators.domain_generator import DomainGenerator
import logging
logging.basicConfig(level=logging.DEBUG)
import uuid

INPUT_FILE_NAME = 'data/inputs/sample_intents.csv'

def read_intents():
    intents = []
    logging.debug('Reading intents...')
    with open(INPUT_FILE_NAME, 'r') as read_obj: 
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            intent = row
            intent['intent_name'] = str(uuid.uuid4().hex)
            intents.append(intent)
    return intents

def main():
    # read sample intents
    intents = read_intents()

    # generate NLUs
    logging.debug('Generating NLU...')
    NLUEGenerator().generate(intents)

    # generate domain
    logging.debug('Generating domain...')
    DomainGenerator().generate(intents)

    logging.debug('Completed, please check output folder for results.')
    
if __name__ == "__main__":
    main()