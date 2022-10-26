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
    
    person, label, confidence_score = entity['word'], entity['entity_group'], entity['score']
    
    is_present= False
    is_weird = False
    new_entities = []
    
    with open("data/artists_db.txt", encoding="utf8") as file:
        artists_db = file.read().split("\n")
        file.close() 
    
    if mode=='outer':
        
        if person in artists_db:
            print("Present in DB: list check --> ",person)

            is_present= True

        else:
            for artists in artists_db:
                if levenshtein_distance(artists,person) <2 :
                    print("Present in DB: distance check")
                    print(artists,person)       
                    is_present= True
                    
                    break
            
                elif len(person) > 15 and label == 'MISC' and confidence_score < 0.90:
                    if artists+' ' in person or artists+',' in person or artists+'/' in person:
                        print("Artist present in parts of sentence")
                        print(artists,person.replace(artists,"").lstrip())
                        new_words = [artists,person.replace(artists,"").lstrip()]
                        for word in new_words:
                            new_entities.append(ner(word)[0])

                        is_present= False
                        is_weird = True

        return is_present, is_weird, new_entities
    
    elif mode == 'inner':
        
        if person in artists_db:
            print("Present in DB: list check --> ",person)

            is_present= True

        else:
            for artists in artists_db:
                if levenshtein_distance(artists,person) <2 :
                    print("Present in DB: distance check")
                    print(artists,person)       
                    is_present= True
                    break        
        
        return is_present

def assign_labels(entity,output):
    
    if entity['entity_group'] == 'PER' and entity['score'] > 0.75:
        output['artists'].append(entity['word'])
        update_db(entity['word'])
    elif entity['entity_group'] == 'PER' and entity['score'] < 0.75:
        output['artists'].append(entity['word'])               
    elif entity['entity_group'] == 'ORG':
        output['events'].append(entity['word'])
    elif entity['entity_group'] == 'MISC'and len(entity['word']) >= 2:
        output['events'].append(entity['word'])
    elif entity['entity_group'] == 'LOC':
        output['location'].append(entity['word'])
        
    return output

def handle_new_entities(new_entities, ner, output):
    for new_entity in new_entities:
        if new_entity['entity_group']!= 'DATE':
            is_present = check_db(new_entity, ner, mode='inner')
            if is_present:
                output['artists'].append(new_entity['word'])
            else:
                output = assign_labels(new_entity,output)
        else:
            output['date'].append(new_entity['word'])            
                        
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
        
        if entity['entity_group']== 'MISC' and entity['score'] < 0.70:
            pass
        
        elif entity['entity_group']!= 'DATE':
            is_present, is_weird, new_entities = check_db(entity, ner, mode='outer')
            
            if is_present:
                if entity['score'] > 0.50:
                    output['artists'].append(entity['word'])
                    #print("is present", entity['word'])
                
            elif is_weird:
                #print(new_entities)
                output = handle_new_entities(new_entities, ner, output)
                
            else:
                output = assign_labels(entity,output)
                #print("assign labels", entity['word'])
                
        else:
            output['date'].append(entity['word'])
            
            
    output = remove_duplicates(output)
    return output