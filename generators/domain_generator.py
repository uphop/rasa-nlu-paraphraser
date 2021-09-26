import os
import sys
import ruamel
import ruamel.yaml
from ruamel.yaml.scalarstring import PreservedScalarString as pss
from shutil import copyfile, copytree, rmtree

'''
Generates Rasa domain based on template
'''
class DomainGenerator:
    def __init__(self):
        # get input / ouput details from config
        self.TEMPLATE_FOLDER = os.getenv('TEMPLATE_FOLDER', './data/templates')
        self.OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', './data/output')
        self.TEMPLATE_DOMAIN_FILE = os.getenv('TEMPLATE_DOMAIN_FILE', 'domain.yml')
        self.OUTPUT_DOMAIN_FILE = os.getenv('OUTPUT_DOMAIN_FILE', 'domain.yml')

    def generate(self, intents):
        # re-create output folder
        if not os.path.exists(self.OUTPUT_FOLDER):
            os.makedirs(self.OUTPUT_FOLDER)

        domain_output_file = self.prepare_domain_output_file()

        # init YAML
        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = False

        # open copied template and load YAML
        with open(domain_output_file, 'r') as stream:
            documents = yaml.load(stream)

        # add current basket items to the responses section of the YAML document
        for intent in intents:
            # prepare a new intent element
            intent_item, text = self.get_intent_domain(intent['intent_name'], intent['intent_original_response'])

            # add intent and response to the doc
            documents['intents'].append(intent['intent_name'])
            documents['responses'][intent_item] = text

        # save intents back to the output YAML file
        with open(domain_output_file, 'w') as file:
            yaml.dump(documents, file)

        # return output file path
        return domain_output_file
    
    def prepare_domain_output_file(self):
        # make a copy of domain template
        domain_template_file = self.TEMPLATE_FOLDER + '/' + self.TEMPLATE_DOMAIN_FILE
        domain_output_file = self.OUTPUT_FOLDER + '/' + self.OUTPUT_DOMAIN_FILE
        
        try:
            copyfile(domain_template_file, domain_output_file)
        except OSError as err:
            print("Error: % s" % err)

        return domain_output_file
    
    def get_intent_domain(self, intent_name, intent_orignal_response):
        # prepare a new intent element
        intent = 'utter_' + intent_name
        text = [{'text': intent_orignal_response}]
        return intent, text