import os

# full database file path
db = os.path.dirname(__file__) + '/wolfie_home.db'

"""
This is global that stores singletones.
use @singletone decorator to singletone classes.
"""
def singletone(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()
