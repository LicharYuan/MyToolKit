""" Script to handle IO. """
import pickle
import os
import json
import pathlib

def get_file_stat(filepath):
   fname = pathlib.Path(filepath) 
   assert fname.exists(), f'No such file: {fname}'
   print(fname.stat()) 

def load_pkl(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_filename(filename):
    # abs path or relative path
    check_path(os.path.dirname(filename))
    if not os.path.exists(filename):
        Path(filename).touch()


def save_to_pkl(save_path, save_content, save_name="dict"):
    check_path(save_path)
    assert isinstance(save_name, str)
    filepath = os.path.join(save_path, save_name+".pkl")
    with open(filepath, 'wb') as f:
        pickle.dump(save_content, f)
    return filepath

def save_to_json(save_path, save_content, save_name="tmpjson"):
    check_path(save_path)
    assert isinstance(save_name, str)
    filepath = os.path.join(save_path, save_name+".json")
    with open(filepath, 'w') as f:
        json.dump(save_content, f)
    return filepath

def append_to_txt(ori_file, new_lines):
    with open(ori_file, 'a') as f:
        f.write(new_lines+'\n')
    