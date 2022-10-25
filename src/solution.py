from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import timeit
import utils

# Solution adopted from --> https://huggingface.co/Jean-Baptiste/camembert-ner-with-dates
start = timeit.default_timer()

tokenizer = AutoTokenizer.from_pretrained("./models/tokenizer/")
model = AutoModelForTokenClassification.from_pretrained("./models/model/")

ner = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

sample_event = "Jojo Mayer / Nerve w/ DJ HA at MilkBoy 3/15"

entities = ner(sample_event)
json_out = utils.check_entities(entities, ner)

print("Entities:",entities)
print("JSON_OUTPUT:",json_out)

stop = timeit.default_timer()
print('Time taken: ', stop - start) 