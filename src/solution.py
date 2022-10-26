from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

import os
import os.path as osp
import timeit
import argparse
import json
from datetime import datetime

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
    print("Entities:",entities)

    return json_out

if __name__ == '__main__':
    """     parser = argparse.ArgumentParser(description="Information extraction from Event titles.")
        parser.add_argument("event", action = 'store', type = str, nargs='+', 
        default='Jan Beuving & Patrick Nederkoorn - Leuker Kunnen We Het Niet Maken', help="Enter event titles for information extraction!")

        FLAGS  = parser.parse_args()
        event_title = ' '.join(FLAGS.event)

        start = timeit.default_timer()

        print(event_title)
        json_out = extract_entities(event_title)
        print(json_out)

        stop = timeit.default_timer()
        print('Time taken: ', stop - start)  """

    with open("./data/event_titles.txt", encoding="utf8") as file:
        events = file.read().split("\n")
        file.close() 

    out = []
    start = timeit.default_timer()
    count = 0
    for event in events[:5]:
        out.append(extract_entities(event))
        count = count + 1
        
        if count%100 == 0:
            print(f"Events done: {count}/{len(events)}")
    
    save_path = f'./outputs/'
    if not osp.exists(save_path):
        os.mkdir(save_path)

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")

    with open(f"./outputs/{dt_string}_artists_events.json", "w") as final:
        json.dump(out, final, indent = 5)
    print("JSON DUMP COMPLETE")
    stop = timeit.default_timer()
    print('Time: ', stop - start) 
  
    



