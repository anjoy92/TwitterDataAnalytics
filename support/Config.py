import json

class Config(object):
    def __init__(self,root):
        self.root=root
        with open(self.root+'config.json') as json_data_file:
            self.data = json.load(json_data_file)

    def Write(self):
        with open(self.root+'config.json', 'w') as outfile:
            outfile.write(json.dumps(self.data, indent=4, sort_keys=True))