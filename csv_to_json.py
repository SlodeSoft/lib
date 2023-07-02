class csv_to_json:
    def __init__(self, file):
        '''
        :param file: chemin du fichier .csv à convertir en list de dict,
        utile dans l'utilisation de ZingGrid
        '''
        self.file = file

    def convert_csv_dict(self):
        with open(self.file, 'r', encoding='utf-8') as csv:
            first_line = csv.readline()
            out = csv.readlines()
        final_output = list()
        for x in out:
            final_output.append(dict(zip(first_line.split(','), x.replace('\n', '').split(','))))
        return final_output
