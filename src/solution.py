from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

import os
import json
import os.path as osp
import timeit
from datetime import datetime

import utils

EVENTS_DB = './data/event_titles.txt'

# Solution adopted from --> https://huggingface.co/Jean-Baptiste/camembert-ner-with-dates

tokenizer = AutoTokenizer.from_pretrained("./models/tokenizer/")
model = AutoModelForTokenClassification.from_pretrained("./models/model/")
ner = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def extract_entities(event_title):

    output = {
    'event_name': event_title, # returning event name to user
    'artists':[],              # to be filled with artists lineup
    'event_info':[],           # to be filled with event details if available
    'location':[],             # to be filled with location details if available
    'date':[],                 # to be filled with date and time if available
    'related_keywords':[]      # to be filled with unclassified keywords
}
    if len(event_title) !=0:
        event_title = utils.clean_sentence(event_title)
        entities = ner(event_title)
        json_out = utils.check_entities(entities, ner, event_title, output, mode='outer')

    return json_out

# function to test model with event_titles database
def extract_from_file(file_path):

    with open(file_path, encoding="utf8") as file:
        events = file.read().split("\n")
        file.close() 

    out = []
    start = timeit.default_timer()
    count = 0
    for event in events:
        out.append(extract_entities(event))
        count = count + 1
        if count%100 == 0:
            print(f"Events done: {count}/{len(events)}")

    save_path = f'./outputs/'
    if not osp.exists(save_path):
        os.mkdir(save_path)

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")

    with open(f"./outputs/{dt_string}_artists_events.json", "w", encoding='utf-8') as final:
        json.dump(out, final, indent = 5)
    print("JSON DUMP COMPLETE")
    stop = timeit.default_timer()
    print('Time: ', stop - start) 

# to test the code, uncomment and run the below line
# extract_from_file(EVENTS_DB)