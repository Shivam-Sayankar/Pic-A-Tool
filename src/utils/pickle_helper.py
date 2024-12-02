import pickle

def load_pickle(file_path):
    
    with open(file_path, "rb") as file:
        pickle_data = pickle.load(file)

        return pickle_data