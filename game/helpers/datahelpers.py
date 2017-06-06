# helper module to manage loading/saving game data
import json
import glob
from collections import defaultdict
from os.path import basename


def get_all_from_dir(dir):
    list_out = []
    for file in glob.glob(dir+"/*.json"):
        name = basename(file).split(".")[0]
        list_out.append([name, load_json(file)])
    return list_out


def save_json(json_path, json_dict):
    with open(json_path, 'w') as fo:
        json.dump(json_dict, fo, indent=2,
                  sort_keys=True, separators=(',', ':'))


def load_json(json_path):
    with open(json_path) as fn:
        json_dict = json.load(fn)
        better_dict = defaultdict(lambda: {}, json_dict)
    return better_dict
