import os
import json
import os.path as osp
from datetime import datetime

from src.solution import extract_entities
from testEvents import test_dict


test_output = {}

for key in test_dict.keys():
    print(f"Running tests for test case {key}")

    list_for_test_cases = []
    for event in test_dict[key]:
        list_for_test_cases.append(extract_entities(event))

    test_output[key] = []
    test_output[key] = list_for_test_cases

now = datetime.now()
dt_string = now.strftime("%d%m%Y_%H%M%S")

save_path = f'./outputs/'
if not osp.exists(save_path):
    os.mkdir(save_path)

with open(f"./outputs/{dt_string}_test_artists_events.json", "w", encoding='utf-8') as final:
    json.dump(test_output, final, indent = 6)

print("JSON DUMP COMPLETE")

