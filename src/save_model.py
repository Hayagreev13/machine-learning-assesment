from transformers import AutoTokenizer, AutoModelForTokenClassification

# Solution adopted from --> https://huggingface.co/Jean-Baptiste/camembert-ner-with-dates
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
tokenizer.save_pretrained("./models/tokenizer/")

model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
model.save_pretrained("./models/model/")