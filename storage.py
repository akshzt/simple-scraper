from abc import ABC, abstractmethod
import json
import os

class StorageInterface(ABC):
    @abstractmethod
    def save_data(self, data):
        pass

class JSONStorage(StorageInterface):
    def __init__(self, filename="data.json"):
        self.filename = filename

    def save_data(self, data):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_data.extend(data)

        with open(self.filename, "w") as f:
            json.dump(existing_data, f, indent=4)
