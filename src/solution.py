from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

import utils

# Solution adopted from --> https://huggingface.co/Jean-Baptiste/camembert-ner-with-dates
'''start = timeit.default_timer()'''

tokenizer = AutoTokenizer.from_pretrained("./models/tokenizer/")
model = AutoModelForTokenClassification.from_pretrained("./models/model/")
ner = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def extract_entities(event_title):

    event_title = utils.clean_sentence(event_title)
    entities = ner(event_title)
    json_out = utils.check_entities(entities, ner, event_title)
    #print("Entities:",entities)

    return json_out