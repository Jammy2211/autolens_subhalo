from itertools import islice
import json
import pickle
import os
from os import path

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


pickle_path = path.join("paper", "to_json")
pickle_file = path.join(pickle_path, "slopes.pkl")

with open(
        os.path.join(pickle_file), "rb"
) as f:
    slopes = pickle.load(f)

slope_all_dict = slopes.to_dict()

def convert_to_bells(value_dict):

    slope_dict = {}

    for i, (key, value) in enumerate(value_dict.items()):

        if i > 41:

            slope_dict[key] = value_dict[key]

    return {key.replace("J", "SDSSJ"): value for key, value in slope_dict.items()}

slope_dict = convert_to_bells(value_dict=slope_all_dict["slope"])
slope_ue3_dict = convert_to_bells(value_dict=slope_all_dict["ue3_slope"])
slope_le3_dict = convert_to_bells(value_dict=slope_all_dict["le3_slope"])

json_path = path.join("paper", "json")

slope_dict_file = path.join(json_path, "amy", f"slope_dict.json")
slope_ue3_dict_file = path.join(json_path, "amy", f"slope_dict_ue3.json")
slope_le3_dict_file = path.join(json_path, "amy", f"slope_dict_le3.json")

with open(slope_dict_file, "w+") as f:
    json.dump(slope_dict, f, indent=4)

with open(slope_ue3_dict_file, "w+") as f:
    json.dump(slope_ue3_dict, f, indent=4)

with open(slope_le3_dict_file, "w+") as f:
    json.dump(slope_le3_dict, f, indent=4)