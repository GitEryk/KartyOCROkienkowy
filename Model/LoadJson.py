import json
from tkinter import filedialog


class LoadJson:
    def __init__(self):
        self.file_pathJson = None

    def importSetting(self, path=None):
        if path is None:
            self.file_pathJson = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        else:
            self.file_pathJson = path

        if self.file_pathJson:
            with open(self.file_pathJson, 'r') as file:
                try:
                    data = json.load(file)
                    label = "Załadowano plik"
                    return data, label
                except json.JSONDecodeError as e:
                    print(f"Błąd dekodowania pliku JSON: {e}")
                    label = f"Błąd dekodowania pliku JSON: {e}"
                    return None, label
        else:
            label = "Proszę wybrać plik JSON."
            return None, label

    def exportSetting(self, data):
        json_data = data
        self.file_pathJson = filedialog.asksaveasfile(initialfile='own_setting.json', defaultextension=".json",
                                                      filetypes=[("JSON files", "*.json")])
        newJson = self.file_pathJson.name.split("/")
        newJson = newJson[-1]
        newJson = newJson.split(".")
        newJson = newJson[0]
        json_data['name'] = newJson
        if self.file_pathJson is not None:
            with open(self.file_pathJson.name, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)

    def takePath(self, path):
        self.file_pathJson = path
        return self.file_pathJson

    def getPath(self):

        return self.file_pathJson