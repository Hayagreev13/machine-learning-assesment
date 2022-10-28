from Levenshtein import distance as levenshtein_distance

import re
import os
import os.path as osp
import logging
from datetime import datetime

ARTISTS_DB = './data/artists_db.txt'

# setting up logging
now = datetime.now()
dt_string = now.strftime("%d%m%Y_%H%M%S")
        
save_path = f'./logs/'
if not osp.exists(save_path):
    os.mkdir(save_path)
        
logging.basicConfig(filename = f'logs/{dt_string}_run_log.log',
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()

def clean_sentence(sentence):
    # removes weird characters and adds sense to sentences
    
    sentence = sentence.replace('w/','with')
    sentence = sentence.replace(' w ',' with ')
    sentence = sentence.replace('@','at ')
    sentence = sentence.replace('~',', ')
    sentence = sentence.replace(' • ',' | ')
    sentence = sentence.replace('•',' ')
    sentence = sentence.replace('''"''',"'")
    sentence = sentence.replace("„","'")
    sentence = sentence.replace("“", "'")
    
    return sentence


def check_entities(entities, ner, event_title):
    # function to check and classify all the entities obtained after NER
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
        logger.info(f"Entity: {entity}")

        if label == 'PER':
            output = check_person(entity, output)
        elif label == 'LOC':
            output = check_location(entity, ner, event_title, output)
        if label == 'ORG':
            output = check_org(entity, ner, event_title, output)
        elif label == 'DATE':
            output['date'].append(entity['word'])
        elif label == 'MISC':
            output = check_misc(entity, ner, event_title, output, mode='outer')

        del label
        logger.info('-------------------------------------------------------------------------------------------------------------------')
    output = remove_duplicates(output)
    return output

def update_db(person):
    # updates database with new artists
    with open(ARTISTS_DB, "a+", encoding='utf-8') as file:
        file.seek(0)
        database = file.read()
        if person not in database:
            file.write ("\n"+person)
            logger.info(f"Artist updated to database: {person}")
        file.close()   

def check_db(potential_artist):
    # function to check database and calculate distance between 2 words using levenshtein distance
    method = None
    
    with open("data/artists_db.txt", encoding="utf8") as file:
        artists_db = file.read().split("\n")
        file.close() 
        
    if potential_artist in artists_db:
        logger.info(f"Present in DB: {potential_artist}")
        method = 'present'

    else:
        for artists in artists_db:
            if levenshtein_distance(artists,potential_artist) <2 :
                logger.info(f"Passed distance check: {artists}, {potential_artist}")    
                method = 'distance'
                break        

    return method


def check_person(entity, output):
    # function to check PER entities, not capable of extracting new entities
    potential_artist, confidence_score = entity['word'], entity['score']
    database_check = check_db(potential_artist)
    
    if database_check == 'present':
        output['artists'].append(potential_artist)
        logger.info(f"Person present in artist DB: {potential_artist}")
        
    elif database_check == 'distance' and confidence_score > 0.60:
        output['artists'].append(potential_artist)
        logger.info(f"Person passed distance check and confidence > 0.60: {potential_artist}")
        
    elif confidence_score > 0.75:
        output['artists'].append(potential_artist)
        update_db(potential_artist)
        logger.info(f"Person with confidence > 0.75 added to database: {potential_artist}")
        
    elif confidence_score < 0.75 and confidence_score > 0.60:
        output['artists'].append(potential_artist)
        logger.info(f"Person with confidence 0.75-0.60 classified as artist: {potential_artist}")

    else:
        output['related_keywords'].append(potential_artist)
        logger.info(f"Person unclassified: {potential_artist}")
        
    del potential_artist, confidence_score, database_check 
    return output

    
def check_location(entity, ner, event_title, output):
    # function to LOC check entities, capable of extracting new entities

    potential_location, confidence_score = entity['word'], entity['score']
    word_to_event_title_ratio = len(potential_location)/len(event_title)
    
    if word_to_event_title_ratio > 0.80:
        is_present, new_entities = extract_new_entities(entity, ner, mode='low')

        if not is_present:
            output['location'].append(potential_location)
            logger.info(f"Location classified with misc ratio > 0.80: {potential_location}")

        else:
            output = process_new_entities(new_entities, ner, event_title, output)
            logger.info(f"Location processing new entities with misc ratio > 0.80: {new_entities}")        
    
    elif confidence_score > 0.70:
        output['location'].append(potential_location)
        logger.info(f"Location with confidence score >0.70: {potential_location}")
        
    elif check_db(potential_location) == 'present':
        output['artists'].append(potential_location)
        logger.info(f"Location present in artist DB: {potential_location}")
        
    elif check_db(potential_location) == 'distance' and confidence_score > 0.60:
        output['event_info'].append(potential_location)
        logger.info(f"Location passing distance check in artist DB: {potential_location}")
        
    else:
        output['related_keywords'].append(potential_location)
        logger.info(f"Location unclassified: {potential_location}")
        
    del potential_location, confidence_score
    return output


def check_org(entity, ner, event_title, output):
    # function to check ORG entities, capable of extracting new entities

    event_info, confidence_score = entity['word'], entity['score']
    word_to_event_title_ratio = len(event_info)/len(event_title)
    
    database_check = check_db(event_info)
    
    if database_check == 'present':
        output['artists'].append(event_info)
        logger.info(f"Organisation present in artist DB: {event_info}")
        
    elif database_check == 'distance' and confidence_score > 0.60:
        output['artists'].append(event_info)
        logger.info(f"Organisation passed distance check and confidence > 0.60: {event_info}")
        
    elif confidence_score > 0.70:
        if word_to_event_title_ratio < 0.80:
            
            output['event_info'].append(event_info)
            logger.info(f"Organisation with confidence > 0.70 classified as event info: {event_info}")
            
        else:
            is_present, new_entities = extract_new_entities(entity, ner)
            
            if not is_present:
                output['event_info'].append(event_info)
                logger.info(f"Organisation classified with confidence > 0.70 and misc ratio > 0.80: {event_info}")
                
            else:
                output = process_new_entities(new_entities, ner, event_title, output)
                logger.info(f"Organisation processing new entities with confidence > 0.70: {new_entities}")
        
    else:
        output['related_keywords'].append(event_info)
        logger.info(f"Organisation unclassified: {event_info}")
        
    del event_info, confidence_score, database_check 
    return output


def check_misc(entity, ner, event_title, output, mode=None):
    # function to check MISC entities, capable of extracting new entities

    event_info, confidence_score = entity['word'], entity['score']
    word_to_event_title_ratio = len(event_info)/len(event_title)
    
    database_check = check_db(event_info)
    
    if len(event_info) < 2:
        output['related_keywords'].append(event_info)
        logger.info(f"Misc rejected because of small word length: {event_info}")
    
    elif database_check == 'present':
        output['artists'].append(event_info)
        logger.info(f"Misc present in artist DB: {event_info}")
        
    elif database_check == 'distance' and confidence_score > 0.60:
        output['artists'].append(event_info)
        logger.info(f"Organisation passed distance check and confidence > 0.60: {event_info}")
        
    elif confidence_score > 0.90:
        if word_to_event_title_ratio < 0.70:
            
            output['event_info'].append(event_info)
            logger.info(f"Misc classified with confidence > 0.90: {event_info}")
            
        else:
            is_present, new_entities = extract_new_entities(entity, ner)
            
            if not is_present:
                output['event_info'].append(event_info)
                logger.info(f"Misc classified with confidence > 0.90 and misc ratio > 0.70: {event_info}")
                
            else:
                output = process_new_entities(new_entities, ner, event_title, output)
                logger.info(f"Misc processing new entities with confidence > 0.90: {new_entities}")
        
    elif word_to_event_title_ratio > 0.70 and confidence_score < 0.90 and confidence_score > 0.50 and mode=='outer':
        
        is_present, new_entities = extract_new_entities(entity, ner, mode='low')
        logger.info(f"Misc Extracting new entities: {event_info}")
        
        if is_present:
            output = process_new_entities(new_entities, ner, event_title, output)
            logger.info(f"Misc processing new entities with confidence between 0.90-0.50: {new_entities}")
        else:
            output['related_keywords'].append(event_info)
            logger.info(f"Misc unclassified after checking again: {event_info}")
            
        del is_present, new_entities
        
    else:
        output['related_keywords'].append(event_info)
        logger.info(f"Misc unclassified: {event_info}")
        
    del event_info, confidence_score, word_to_event_title_ratio, database_check 
    return output

def split_sentence(sentence):
    # function used to split a sentence based on /,-,+,:,| and variations of 'and'
    split = []
    best_split = 1
    temp_splits = [sentence.split("/ "), sentence.split(" - "), sentence.split("+"), sentence.split(": "),
    sentence.split("|"), sentence.split(" and "), sentence.split(" And "), sentence.split("& ")]
    
    for temp in temp_splits:
        if len(temp) > best_split:
            split = temp
            best_split = len(temp)
            
    del temp_splits
    return split

def extract_new_entities(entity, ner, mode=None):
    # function to extract new entites from exisiting entities
    # mode = None is used to split the sentence and check the words in the sentence
    # mode = low is used to check split words and to check if artists are present in parts of the sentence

    potential_artist, confidence_score = entity['word'], entity['score']
    
    new_entities = []
    is_present= False
    
    split = split_sentence(potential_artist)
    
    if len(split) > 1:
        logger.info(f"Sentence split for finding new entities: {split}")
        for word in split:
            try:
                new_entities.append(ner(word)[0])
            except:
                pass
        
    elif mode=='low'and len(split) < 1:
        
        with open("data/artists_db.txt", encoding="utf8") as file:
            artists_db = file.read().split("\n")
            file.close()

        for artist in artists_db:
            if artist+' ' in potential_artist or artist+',' in potential_artist or artist+'/' in potential_artist \
            or artist+"'" in potential_artist:
                logger.info(f"Artist present in parts of sentence : {artist},{potential_artist}")
                #print(f"Artist present in parts of sentence : {artist}, {potential_artist}")
                new_words = [artist,potential_artist.replace(artist,"").strip("-&")]
                for word in new_words:
                    try:
                        new_entities.append(ner(word)[0])
                    except:
                        pass
                    
    
    if len(new_entities) >= 1:
        is_present = True
            
    del potential_artist, confidence_score 
    return is_present, new_entities

def process_new_entities(new_entities, ner, event_title, output):
    # function to check and classify newly found entities
    for new_entity in new_entities:

        logger.info(f"Entity: {new_entity}")
        label= new_entity['entity_group']
        
        if label == 'PER':
            output = check_person(new_entity, output)
        elif label == 'LOC':
            output = check_location(new_entity, ner, event_title, output)
        if label == 'ORG':
            output = check_org(new_entity, ner, event_title, output)
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
            
    if len(output['artists']) !=0 and len(output['related_keywords']) !=0:
        
        for artist in output['artists']:
            for keyword in output['related_keywords']:
                if artist in keyword:
                    keyword = keyword.replace(artist,'')
            
    return output