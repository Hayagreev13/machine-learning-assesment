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

def check_db(entity, ner, mode='outer'):
    # checks database if artist is present based on presence, word distances and confidence scores
    potential_artist, label, confidence_score = entity['word'], entity['entity_group'], entity['score']
    
    is_present= False
    is_weird = False
    new_entities = []
    
    with open("data/artists_db.txt", encoding="utf8") as file:
        artists_db = file.read().split("\n")
        file.close() 
    
    if mode=='outer':
        # triggered when ner is performed for the first time in check_entities; capable of checking database and identifying new entities
        # returns boolean values and potential new entities
        if potential_artist in artists_db:
            logger.info(f"Present in DB: list check --> {potential_artist}")
            print("Present in DB: list check --> ",potential_artist)
            is_present= True

        else:
            for artists in artists_db:
                if levenshtein_distance(artists,potential_artist) <2 :
                    logger.info(f"Present in DB: distance check : {artists}, {potential_artist}")
                    print("Present in DB: distance check")
                    print(artists,potential_artist)       
                    is_present= True
                    
                    break
            
                elif len(potential_artist) > 15 and label == 'MISC' and confidence_score < 0.90 and confidence_score > 0.60:
                    if artists+' ' in potential_artist or artists+',' in potential_artist or artists+'/' in potential_artist:
                        logger.info(f"Artist present in parts of sentence : {artists}, {potential_artist}")
                        print("Artist present in parts of sentence")
                        print(artists,potential_artist.replace(artists,"").lstrip())
                        new_words = [artists,potential_artist.replace(artists,"").lstrip()]
                        for word in new_words:
                            try:
                                new_entities.append(ner(word)[0])
                            except:
                                pass

                        is_present= False
                        is_weird = True
                        
        del potential_artist, label, confidence_score
        return is_present, is_weird, new_entities
    
    elif mode == 'inner':
        # triggered when ner is performed for the second time in process_new_entities; not capable of identifying new entities
        # returns boolean value based on the presence of artist in the database
        if potential_artist in artists_db:
            print("Present in DB: list check --> ",potential_artist)
            logger.info(f"Present in DB: list check --> {potential_artist}")

            is_present= True

        else:
            for artists in artists_db:
                if levenshtein_distance(artists,potential_artist) <2 :
                    logger.info(f"Present in DB: distance check : {artists}, {potential_artist}")
                    print("Present in DB: distance check")
                    print(artists,potential_artist)       
                    is_present= True
                    break        
        
        del potential_artist, label, confidence_score
        return is_present

def assign_labels(entity,output):
    # assigns final labels to extracted entities based on existing labels and confidence scores
    event_info, label, confidence_score = entity['word'], entity['entity_group'], entity['score']
    
    if label == 'PER' and confidence_score > 0.75:
        output['artists'].append(event_info)
        update_db(event_info)
    elif label == 'PER' and confidence_score < 0.75 and confidence_score > 0.60:
        output['artists'].append(event_info)               
    elif label == 'ORG':
        output['events'].append(event_info)
    elif label == 'MISC'and len(event_info) >= 2:
        output['events'].append(event_info)
    elif label == 'LOC':
        output['location'].append(event_info)
        
    del event_info, label, confidence_score
    return output

def process_new_entities(new_entities, ner, output):
    # function to process newly extracted entities from check_db - outer mode
    for new_entity in new_entities:
        
        event_info, label, confidence_score = new_entity['word'], new_entity['entity_group'], new_entity['score']
        
        if label == 'MISC' and confidence_score < 0.70:
            pass

        elif label != 'DATE':
            is_present = check_db(new_entity, ner, mode='inner')
            
            if is_present:
                if confidence_score > 0.60:
                    output['artists'].append(event_info)
            else:
                output = assign_labels(new_entity,output)
        else:
            output['date'].append(event_info)
            
    del event_info, label, confidence_score
    return output 

def remove_duplicates(output):
    # removes duplicates from final output
    for key in output.keys():
        if key != 'event_name':
            output[key] = [*set(output[key])]
            
    return output

def check_entities(entities, ner, sample):
    # checks, filters and assigns labels to extracted entities
    output = {
        'event_name': sample, #returning event name to user
        'artists':[],  # to be filled with artists lineup
        'events':[],   # to be filled with event details if available
        'location':[], # to be filled with location details if available
        'date':[]      # to be filled with date and time if available
    }
    
    for entity in entities:
        
        event_info, label, confidence_score = entity['word'], entity['entity_group'], entity['score']
        logger.info(f"Entity: {entity}")
        if label == 'MISC' and confidence_score < 0.70:
            pass
        
        elif label != 'DATE':
            is_present, is_weird, new_entities = check_db(entity, ner, mode='outer')
            
            if is_present:
                if confidence_score > 0.60:
                    output['artists'].append(event_info)
                    logger.info(f" is present in db with confidence score > 60% : {event_info}")
                    #print("is present", entity['word'])
                
            elif is_weird:
                #print(new_entities)
                logger.info(f"New Entities found: {new_entities}")
                output = process_new_entities(new_entities, ner, output)
                
            else:
                output = assign_labels(entity,output)
                logger.info(f"Assigned labels via assign_labels: {event_info}")
                #print("assign labels", entity['word'])
                
        else:
            output['date'].append(event_info)
            
        del event_info, label, confidence_score
    logger.info("---------------------------------------------------------------------------------------------------------------------")
    output = remove_duplicates(output)
    return output