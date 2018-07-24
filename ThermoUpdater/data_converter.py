#  Cron Job made to process data from Access DB and Post cleaned data to updater website

import xlrd
import requests
import time


#  Relevant columns to import from .xlsx sheet
#  As of 7/13/18 the expected format is [projectCode,cleaved,purified,AAA]
#  Section A
columns = [1, 3, 5, 7]
#  As of 7/13/18 the expected format for columns[1:] is a date, currently
#  interpreted as a float on import, possible site of future breakdown
active_type = 'float'


class UpdateConverter:

    #  Imports from directory containing one xlsx file and crops data to fit Section A format
    #  Parameter (CWD + File location)
    #  Returns List of cleaned data
    def import_file(self, directory):
        book = xlrd.open_workbook(directory)
        sheet = book.sheet_by_index(0)
        storage = []
        for i in range(1, sheet.nrows):
            temp_row = []
            for j in range(len(columns)):
                    if active_type in str(type(sheet.cell_value(i, columns[j]))):
                        temp_row.append('x')
                    else:
                        temp_row.append(sheet.cell_value(i, columns[j]))
            storage.append(temp_row)
        return storage

    #  Creates flattened list of current projects represented in imported xlsx sheet
    #  Parameter (list returned from self.import_file() )
    #  Returns Flattened list format [[projectCode,cleaved,purified,AAA],...]
    def organize_data(self, active_list):
        # Creates reference list of current project codes
        codes = []
        for i in range(len(active_list)):
            if active_list[i][0] not in codes:
                codes.append(active_list[i][0])
            else:
                pass

        # Clusters all like project codes into 1 list, format [[projectCode,[x,x,x],[x,x,x],...],...]
        final_list = []
        for j in range(len(codes)):
            temp = []
            temp.append(codes[j])
            for i in range(len(active_list)):
                if active_list[i][0] in codes[j]:
                    temp.append(active_list[i][1:4])
            final_list.append(temp)

        # Adds up Values for individual projectCodes, format [[projectCode, [0, 0, 0, 'of 7']],...
        for i in range(len(final_list)):
            temp_name = final_list[i].pop(0)
            temp_total = len(final_list[i])
            temp_bin = [0,0,0,temp_total]
            for j in range(len(final_list[i])):
                for k in range(0,3):
                    if final_list[i][j][k] == 'x':
                        temp_bin[k] = temp_bin[k] + 1
                else:
                    pass
            final_list[i] = [temp_name, temp_bin]

        #Flattens final list to usable form
        for i in range(len(final_list)):
            temp = final_list[i].pop(1)
            for j in range(0, 4):
                final_list[i].append(temp[j])
        return final_list

    #  Creates individual dictionary containing all information needed for post Pre JSONify
    #  Parameters (flattened_list from organize_data, db id used during POST request)
    #  Returns dictionary
    def create_JSON_string(self, flattened_list, database_index):
        return {"AAA": str(flattened_list[3]), "cleaved": str(flattened_list[1]), "purified": str(flattened_list[2]),
                "projectCode": str(flattened_list[0]), "id": str(database_index),
                "resource_uri": str("/login/api/log/%s/" % database_index), "totalProjects": str(flattened_list[4])}


    #  Performs individual Post requests
    #  Parameters (individual flattened JSON prepped Dictionary)
    #  Return, void
    def post(self, data):
        url = 'http://localhost:8000/login/api/log/'
        r = requests.post(url, json=data)
#  keep for debugging purposes
        #print(r.text)
        rt = requests.get(url)
        print(rt.text)

    def post_iterator(self,post_list):
        for i in range(len(post_list)):
            update_info = self.create_JSON_string(post_list[i], i)
            self.post(update_info)
            #time.sleep(1)
        url = 'http://localhost:8000/login/api/log/'
        rt = requests.get(url)
        print(rt.text)


    def __init__(self):
        full_storage = self.import_file("C:\\Users\\erikm\\Desktop\\Update.xls")
        organized_list = self.organize_data(full_storage)
        self.post_iterator(organized_list)


if __name__ == '__main__':
    UpdateConverter()
