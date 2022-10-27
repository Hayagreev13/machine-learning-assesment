from Levenshtein import distance as levenshtein_distance

import re
import os
import os.path as osp
import logging
from datetime import datetime

ARTISTS_DB = './data/artists_db.txt'

""" # setting up logging
now = datetime.now()
dt_string = now.strftime("%d%m%Y_%H%M%S")
        
save_path = f'./logs/'
if not osp.exists(save_path):
    os.mkdir(save_path)
        
logging.basicConfig(filename = f'logs/{dt_string}_run_log.log',
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
logger = logging.getLogger() """

def clean_sentence(val):
    # removes weird characters and adds sense to sentences
    regex = re.compile('^»«•~✦<>')
    sentence = regex.sub('', val)
    sentence = sentence.replace('w/','with')
    sentence = sentence.replace(' w ','with')
    sentence = sentence.replace('@','at ')
    sentence = sentence.replace('~',', ')
    sentence = sentence.replace(' • ',' | ')
    sentence = sentence.replace('•',' ')
    sentence = sentence.replace('''"''',"'")
    sentence = sentence.replace("„","'")
    sentence = sentence.replace("“", "'")
    
    return sentence

def update_db(person):
    # updates databse with new artists
    with open(ARTISTS_DB, "a+", encoding='utf-8') as file:
        file.seek(0)
        database = file.read ()
        if person not in database:
            file.write ("\n"+person)
        file.close()

def check_db(potential_artist):
    
    method = None
    
    with open("data/artists_db.txt", encoding="utf8") as file:
        artists_db = file.read().split("\n")
        file.close() 
        
    if potential_artist in artists_db:
        #logger.info(f"Present in DB: list check --> {potential_artist}")
        print("Present in DB: list check --> ",potential_artist)

        method = 'present'

    else:
        for artists in artists_db:
            if levenshtein_distance(artists,potential_artist) <2 :
                #logger.info(f"Present in DB: distance check : {artists}, {potential_artist}")
                print("Present in DB: distance check")
                print(artists,potential_artist)      
                method = 'distance'
                break        

    return method

def check_location(entity, output):
    
    potential_location, confidence_score = entity['word'], entity['score']
    
    if confidence_score > 0.70:
        output['location'].append(potential_location)
        
    elif check_db(potential_location) == 'present':
        output['artist'].append(potential_location)
        
    elif check_db(potential_location) == 'distance' and confidence_score > 0.60:
        output['event_info'].append(potential_location)
        
    else:
        output['related_keywords'].append(potential_location)
        
    del potential_location, confidence_score
    return output

def check_person(entity, output):
    
    potential_artist, confidence_score = entity['word'], entity['score']
    
    database_check = check_db(potential_artist)
    
    if database_check == 'present':
        output['artists'].append(potential_artist)
        
    elif database_check == 'distance' and confidence_score > 0.60:
        output['artists'].append(potential_artist)
        
    elif confidence_score > 0.75:
        output['artists'].append(potential_artist)
        update_db(potential_artist)
        
    elif confidence_score < 0.75 and confidence_score > 0.60:
        output['artists'].append(potential_artist)

    else:
        output['related_keywords'].append(potential_artist)
        
    del potential_artist, confidence_score, database_check 
    return output

def check_org(entity, output):

    event_info, confidence_score = entity['word'], entity['score']

    database_check = check_db(event_info)
    
    if database_check == 'present':
        output['artists'].append(event_info)
        
    elif database_check == 'distance' and confidence_score > 0.60:
        output['artists'].append(event_info)
        
    elif confidence_score > 0.70:
        output['event_info'].append(event_info)
        
    else:
        output['related_keywords'].append(event_info)
        
    del event_info, confidence_score, database_check 
    return output

def check_misc(entity, ner, event_title, output, mode=None):
    
    event_info, confidence_score = entity['word'], entity['score']
    misc_ratio = len(event_info)/len(event_title)
    
    database_check = check_db(event_info)
    
    if len(event_info) < 2:
        output['related_keywords'].append(event_info)
    
    elif database_check == 'present':
        output['artists'].append(event_info)
        
    elif database_check == 'distance' and confidence_score > 0.60:
        output['artists'].append(event_info)
        
    elif misc_ratio > 0.70 and confidence_score < 0.90 and confidence_score > 0.50 and mode=='outer':
        is_present, new_entities = extract_new_entities(entity, ner)
        if is_present:
            output = process_new_entities(new_entities, ner, event_title, output)
        else:
            output['related_keywords'].append(event_info)
            
        del is_present, new_entities
        
    else:
        output['related_keywords'].append(event_info)
        
    del event_info, confidence_score, misc_ratio, database_check 
    return output

def extract_new_entities(entity, ner):
    
    potential_artist, confidence_score = entity['word'], entity['score']
    
    new_entities = []
    is_present= False
    
    with open(ARTISTS_DB, encoding="utf8") as file:
        artists_db = file.read().split("\n")
        file.close()
    
    for artist in artists_db:
        if artist+' ' in potential_artist or artist+',' in potential_artist or artist+'/' in potential_artist:
            #logger.info(f"Artist present in parts of sentence : {artist}, {potential_artist}")
            print(f"Artist present in parts of sentence : {artist}, {potential_artist}")
            new_words = [artist,potential_artist.replace(artist,"").strip("-&")]
            for word in new_words:
                try:
                    new_entities.append(ner(word)[0])
                except:
                    pass
                
            is_present= True
            
    del potential_artist, confidence_score 
    return is_present, new_entities

def process_new_entities(new_entities, ner, event_title, output):
    
    for new_entity in new_entities:
        
        label= new_entity['entity_group']
        
        if label == 'PER':
            output = check_person(new_entity, output)
        elif label == 'LOC':
            output = check_location(new_entity, output)
        if label == 'ORG':
            output = check_org(new_entity, output)
        elif label == 'DATE':
            output['date'].append(new_entity['word'])
        elif label == 'MISC':
            output = check_misc(new_entity, ner, event_title, output)

        del label
        
    output = remove_duplicates(output)
    return output

def remove_duplicates(output):
    # removes duplicates from final output
    for key in output.keys():
        if key != 'event_name':
            output[key] = [*set(output[key])]
            
    return output

def check_entities(entities, ner, event_title):
    
    output = {
        'event_name': event_title, # returning event name to user
        'artists':[],              # to be filled with artists lineup
        'event_info':[],           # to be filled with event details if available
        'location':[],             # to be filled with location details if available
        'date':[],                 # to be filled with date and time if available
        'related_keywords':[]      # to be filled with unclassified keywords
    }
    
    for entity in entities:
        
        label= entity['entity_group']
        
        if label == 'PER':
            output = check_person(entity, output)
        elif label == 'LOC':
            output = check_location(entity, output)
        if label == 'ORG':
            output = check_org(entity, output)
        elif label == 'DATE':
            output['date'].append(entity['word'])
        elif label == 'MISC':
            output = check_misc(entity, ner, event_title, output, mode='outer')

        del label
        
    output = remove_duplicates(output)
    return output