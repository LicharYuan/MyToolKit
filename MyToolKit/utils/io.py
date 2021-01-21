""" Script to handle IO. """
import pickle
import os

def load_pkl(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_to_pkl(save_path, save_dict, save_name='dict'):
    check_path(save_path)
    assert isinstance(save_name, str)
    filepath = os.path.join(save_path, save_name+'.pkl')
    with open(filepath, 'wb') as f:
        pickle.dump(save_dict, f)
    return filepath

