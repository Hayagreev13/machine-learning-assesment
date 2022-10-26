from Levenshtein import distance as levenshtein_distance
import re

ARTISTS_DB = './data/artists_db.txt'

def clean_sentence(val):
    "removes weird characters and adds sense to sentences"
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
    
    return sentence

def update_db(person):
    with open(ARTISTS_DB, "a+", encoding='utf-8') as file:
        file.seek(0)
        database = file.read ()
        if person not in database:
            file.write ("\n"+person)
        file.close()

def check_db(entity, ner, mode='outer'):
    
    potential_artist, label, confidence_score = entity['word'], entity['entity_group'], entity['score']
    
    is_present= False
    is_weird = False
    new_entities = []
    
    with open("data/artists_db.txt", encoding="utf8") as file:
        artists_db = file.read().split("\n")
        file.close() 
    
    if mode=='outer':
        
        if potential_artist in artists_db:
            print("Present in DB: list check --> ",potential_artist)
            is_present= True

        else:
            for artists in artists_db:
                if levenshtein_distance(artists,potential_artist) <2 :
                    print("Present in DB: distance check")
                    print(artists,potential_artist)       
                    is_present= True
                    
                    break
            
                elif len(potential_artist) > 15 and label == 'MISC' and confidence_score < 0.90:
                    if artists+' ' in potential_artist or artists+',' in potential_artist or artists+'/' in potential_artist:
                        print("Artist present in parts of sentence")
                        print(artists,potential_artist.replace(artists,"").lstrip())
                        new_words = [artists,potential_artist.replace(artists,"").lstrip()]
                        for word in new_words:
                            new_entities.append(ner(word)[0])

                        is_present= False
                        is_weird = True
                        
        del potential_artist, label, confidence_score
        return is_present, is_weird, new_entities
    
    elif mode == 'inner':
        
        if potential_artist in artists_db:
            print("Present in DB: list check --> ",potential_artist)

            is_present= True

        else:
            for artists in artists_db:
                if levenshtein_distance(artists,potential_artist) <2 :
                    print("Present in DB: distance check")
                    print(artists,potential_artist)       
                    is_present= True
                    break        
        
        del potential_artist, label, confidence_score
        return is_present

def assign_labels(entity,output):
    
    event_info, label, confidence_score = entity['word'], entity['entity_group'], entity['score']
    
    if label == 'PER' and confidence_score > 0.75:
        output['artists'].append(event_info)
        update_db(event_info)
    elif label == 'PER' and confidence_score < 0.75:
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
    
    for new_entity in new_entities:
        
        event_info, label, confidence_score = new_entity['word'], new_entity['entity_group'], new_entity['score']
        
        if label == 'MISC' and confidence_score < 0.70:
            pass

        elif label != 'DATE':
            is_present = check_db(new_entity, ner, mode='inner')
            
            if is_present:
                if confidence_score > 0.50:
                    output['artists'].append(event_info)
            else:
                output = assign_labels(new_entity,output)
        else:
            output['date'].append(event_info)
            
    del event_info, label, confidence_score
    return output 

def remove_duplicates(output):
    
    for key in output.keys():
        if key != 'event_name':
            output[key] = [*set(output[key])]
            
    return output

def check_entities(entities, ner, sample):
    
    output = {
        'event_name': sample, #returning event name to user
        'artists':[],  # to be filled with artists lineup
        'events':[],   # to be filled with event details if available
        'location':[], # to be filled with location details if available
        'date':[]      # to be filled with date and time if available
    }
    
    for entity in entities:
        
        event_info, label, confidence_score = entity['word'], entity['entity_group'], entity['score']
        
        if label == 'MISC' and confidence_score < 0.70:
            pass
        
        elif label != 'DATE':
            is_present, is_weird, new_entities = check_db(entity, ner, mode='outer')
            
            if is_present:
                if confidence_score > 0.50:
                    output['artists'].append(event_info)
                    #print("is present", entity['word'])
                
            elif is_weird:
                #print(new_entities)
                output = process_new_entities(new_entities, ner, output)
                
            else:
                output = assign_labels(entity,output)
                #print("assign labels", entity['word'])
                
        else:
            output['date'].append(event_info)
            
            
    del event_info, label, confidence_score      
    output = remove_duplicates(output)
    return output