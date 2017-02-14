#@author Nishit Shrestha
import pickle;
import os;
from src.model.InvFile import InvFile;
from nltk.stem.porter import *
class Reader:

    def read_inv_file(self):
        my_dir = os.path.dirname(os.path.dirname(__file__));
        pickle_file_path = os.path.join(my_dir, 'output.txt');
        INV_FILE_HASH = open(pickle_file_path, 'rb');
        obj_dict = pickle.load(INV_FILE_HASH);
        return obj_dict;
