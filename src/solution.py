from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# Solution adopted from --> https://huggingface.co/Jean-Baptiste/camembert-ner-with-dates

tokenizer = AutoTokenizer.from_pretrained("./models/tokenizer/")
model = AutoModelForTokenClassification.from_pretrained("./models/model/")

nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

sample_event = "Jojo Mayer / Nerve w/ DJ HA at MilkBoy 3/15"

print(nlp(sample_event))