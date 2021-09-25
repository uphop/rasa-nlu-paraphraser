import os
import sys
import ruamel
import ruamel.yaml
from ruamel.yaml.scalarstring import PreservedScalarString as pss
from shutil import copyfile, copytree, rmtree
from paraphraser import Paraphraser

'''
Generates Rasa NLU based on template and paraphrases
'''
class NLUEGenerator:
    def __init__(self):
        # get input / ouput details from config
        self.TEMPLATE_FOLDER = os.getenv('TEMPLATE_FOLDER', './templates')
        self.OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', './output')
        self.TEMPLATE_NLU_FILE = os.getenv('TEMPLATE_NLU_FILE', 'nlu.yml')
        self.OUTPUT_NLU_FILE = os.getenv('OUTPUT_NLU_FILE', 'nlu.yml')
        self.TEMPLATE_DOMAIN_FILE = os.getenv('TEMPLATE_DOMAIN_FILE', 'domain.yml')
        self.OUTPUT_DOMAIN_FILE = os.getenv('OUTPUT_DOMAIN_FILE', 'domain.yml')

        # init paraphrase generator
        self.paraphraser = Paraphraser()

    def generate(self, intents):
         # re-create output folder
        if os.path.exists(self.OUTPUT_FOLDER):
            rmtree(self.OUTPUT_FOLDER)
        os.makedirs(self.OUTPUT_FOLDER)

        self.generate_nlu(intents)
        self.generate_domain(intents)
    
    def generate_nlu(self, intents):
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

    def generate_domain(self, intents):
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

    def prepare_nlu_output_file(self):
        # make a copy of NLU template
        nlu_template_file = self.TEMPLATE_FOLDER + '/' + self.TEMPLATE_NLU_FILE
        nlu_output_file = self.OUTPUT_FOLDER + '/' + self.OUTPUT_NLU_FILE

        try:
            copyfile(nlu_template_file, nlu_output_file)
        except OSError as err:
            print("Error: % s" % err)

        return nlu_output_file
    
    def prepare_domain_output_file(self):
        # make a copy of domain template
        domain_template_file = self.TEMPLATE_FOLDER + '/' + self.TEMPLATE_DOMAIN_FILE
        domain_output_file = self.OUTPUT_FOLDER + '/' + self.OUTPUT_DOMAIN_FILE
        
        try:
            copyfile(domain_template_file, domain_output_file)
        except OSError as err:
            print("Error: % s" % err)

        return domain_output_file
    
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
    
    def get_intent_domain(self, intent_name, intent_orignal_response):
        # prepare a new intent element
        intent = 'utter_' + intent_name
        text = [{'text': intent_orignal_response}]
        return intent, text