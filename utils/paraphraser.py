from parrot import Parrot
import torch

class Paraphraser:
    def __init__(self):
       #Init models (make sure you init ONLY once if you integrate this to your code)
        self.parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)

    def get_paraphrases(self, input):
        para_phrases = self.parrot.augment(
            input_phrase = input,
            diversity_ranker="levenshtein",
            do_diverse=True, 
            max_return_phrases = 10, 
            max_length=64, 
            adequacy_threshold = 0.99, 
            fluency_threshold = 0.90
        )

        # add all paraphrased options
        results = [para_phrase[0] for para_phrase in para_phrases]

        return results