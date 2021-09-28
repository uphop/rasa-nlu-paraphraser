from generators.nlu_generator import NLUEGenerator
from generators.domain_generator import DomainGenerator
from utils.intent_reader import IntentReader
from utils.paraphraser import Paraphraser
import logging
logging.basicConfig(level=logging.DEBUG)

def main():
    # init paraphrase generator
    logging.debug('Initializing paraphraser...')
    paraphraser = Paraphraser()

    # read sample intents
    logging.debug('Reading intents...')
    intents = IntentReader().read_intents()

    # generate NLUs
    logging.debug('Generating NLU training data...')
    nlu_output_file = NLUEGenerator(paraphraser).generate(intents)

    # generate domain
    logging.debug('Generating domain data...')
    domain_output_file= DomainGenerator(paraphraser).generate(intents)

    logging.debug('Completed, please check output folder for results: ')
    logging.debug('NLU training data: ' + nlu_output_file)
    logging.debug('Domain data: ' + domain_output_file)
    
if __name__ == "__main__":
    main()