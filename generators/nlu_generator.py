import os
import sys
import ruamel
import ruamel.yaml
from ruamel.yaml.scalarstring import PreservedScalarString as pss
from shutil import copyfile, copytree, rmtree
from utils.paraphraser import Paraphraser

'''
Generates Rasa NLU based on template and paraphrases
'''
class NLUEGenerator:
    def __init__(self):
        # get input / ouput details from config
        self.TEMPLATE_FOLDER = os.getenv('TEMPLATE_FOLDER', './data/templates')
        self.OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', './data/output')
        self.TEMPLATE_NLU_FILE = os.getenv('TEMPLATE_NLU_FILE', 'nlu.yml')
        self.OUTPUT_NLU_FILE = os.getenv('OUTPUT_NLU_FILE', 'nlu.yml')

        # init paraphrase generator
        self.paraphraser = Paraphraser()
    
    def generate(self, intents):
        # re-create output folder
        if not os.path.exists(self.OUTPUT_FOLDER):
            os.makedirs(self.OUTPUT_FOLDER)

        # make a copy of NLU template
        nlu_output_file = self.prepare_nlu_output_file()

        # init YAML
        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = False

        # open copied template and load YAML
        with open(nlu_output_file, 'r') as stream:
            documents = yaml.load(stream)

        # add current basket items to the end of the YAML document
        for intent in intents:
            # prepare a new intent element
            intent_nlu = self.get_intent_nlu(intent['intent_name'], intent['intent_orignal_phrase'])

            # add intent to the doc
            documents['nlu'].append(intent_nlu)

        # save intents back to the output YAML file
        with open(nlu_output_file, 'w') as file:
            yaml.dump(documents, file)

        # return output file path
        return nlu_output_file

    def prepare_nlu_output_file(self):
        # make a copy of NLU template
        nlu_template_file = self.TEMPLATE_FOLDER + '/' + self.TEMPLATE_NLU_FILE
        nlu_output_file = self.OUTPUT_FOLDER + '/' + self.OUTPUT_NLU_FILE

        try:
            copyfile(nlu_template_file, nlu_output_file)
        except OSError as err:
            print("Error: % s" % err)

        return nlu_output_file
    
    def get_intent_nlu(self, intent_name, intent_orignal_phrase):
        # add original phrase
        examples = '- ' + intent_orignal_phrase + '\n'

        # generate parapharses
        paraphrases = self.paraphraser.get_paraphrases(intent_orignal_phrase)

        # concatenate phrase variations
        for paraphrase in paraphrases:
            examples += '- ' + paraphrase + '\n'

        # prepare a new intent element
        intent_nlu = {
            'intent': intent_name,
            'examples': pss(examples)
        }

        return intent_nlu