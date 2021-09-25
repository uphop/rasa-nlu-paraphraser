from csv import DictReader
from nlu_generator import NLUEGenerator

def main():
    # read sample intents
    intents = []
    with open('sample_intents.csv', 'r') as read_obj: 
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            intents.append(row)
            # print(row)

    # generate NLUs
    NLUEGenerator().generate(intents)
    

if __name__ == "__main__":
    main()