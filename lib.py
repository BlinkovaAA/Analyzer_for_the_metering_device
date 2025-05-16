import string
import xml.etree.ElementTree as ET
import os
import pandas as pd

class rt_action():
    
    def __init__ (self, path):
        self.path = ET.parse(path).getroot()
    
    #get table size, name, date_creation
    def protocol_info(filepath:str) -> None:
        filetags = ["name", "created", "xsize", "ysize"]
        output_lines = ["name: ", "date_cration: ", "lines: ", "columns: "]
        for i in range(4):
            print(output_lines[i], filepath.find(filetags[i]).text)

    #return requested channel data
    def extract_channel_data(channel:int, filepath:str) -> list:
        channels_quentity = len(list(filepath.findall("Analysis_Curves/MC/RawData/channels/item/IDChannel")))
        all_channels_data  = list(filepath.findall("Analysis_Curves/MC/RawData/channels/item/tubes/item/data"))
        selected_channel_data = []
        for i in range(len(all_channels_data)):
            selected_channel_data.append(list(map(int, all_channels_data[i].text.split(" ")[:-1])))
        selected_channel_data = selected_channel_data[(len(all_channels_data) // channels_quentity) * channel: 
                                                        (len(all_channels_data) // channels_quentity) * (channel + 1)]
        return selected_channel_data
    
    def search_relationship(channel_name:str, channel_data:list) -> int:
        if channel_name == "fam":
            output = "--------fam-------- \n"
            median_list_even = []
            median_list_non_even = []
            for i in range(0, 16, 2):
                num_even = 0
                num_non_even = 0
                for j in range(i, 384, 16):
                    num_even += max(channel_data[j][7:21]) - min(channel_data[j][7:21])
                    num_non_even += max(channel_data[j + 1][7:21]) - min(channel_data[j + 1][7:21])
                num_non_even /= 192
                median_list_non_even.append(num_non_even)
                num_even /= 192
                median_list_even.append(num_even)
            median_list_even = sorted(median_list_even)
            median_list_non_even = sorted(median_list_non_even)
            median_even = pd.Series(median_list_even).median()
            median_non_even = pd.Series(median_list_non_even).median()
            for i in range(0, 16, 2):
                for j in range(i,384,16):
                    if round((max(channel_data[j][7:21]) - min(channel_data[j][7:21])) / median_even / 100, 2) == 0.06:
                        output += convert_to_table(j) + "\n"
                        print(convert_to_table(j))#Запись в файл
                        output += str(round((max(channel_data[j][7:21]) - min(channel_data[j][7:21])) / median_even / 100, 2)) + "\n"
                    print(round((max(channel_data[j][7:21]) - min(channel_data[j][7:21])) / median_even / 100, 2))#Запись в файл
                for j in range(i+1, 384, 16):
                    if round((max(channel_data[j][7:21]) - min(channel_data[j][7:21])) / median_non_even / 100,2) == 0.06:
                        output += convert_to_table(j) + "\n"
                        print(convert_to_table(j))#Запись в файл
                        output += str(round((max(channel_data[j][7:21]) - min(channel_data[j][7:21])) / median_even / 100, 2)) + "\n"
                        print(round((max(channel_data[j][7:21]) - min(channel_data[j][7:21])) / median_non_even / 100,2))#Запись в файл
            file = open("fam_data.txt", "w")
            file.write(output)
            file.close()
        elif channel_name == "cy5":
            output = "--------cy5-------- \n"
            median_list_even = []
            median_list_non_even = []
            for i in range(0, 16, 2):
                num_even = 0
                num_non_even = 0
                for j in range(i, 384, 16):
                    num_even += max(channel_data[j][9:20]) - min(channel_data[j][9:20])
                    num_non_even += max(channel_data[j + 1][9:20]) - min(channel_data[j + 1][9:20])
                num_non_even /= 192
                median_list_non_even.append(num_non_even)
                num_even /= 192
                median_list_even.append(num_even)
            median_list_even = sorted(median_list_even)
            median_list_non_even = sorted(median_list_non_even)
            median_even = pd.Series(median_list_even).median()
            median_non_even = pd.Series(median_list_non_even).median()
            for i in range(0, 16, 2):
                for j in range(i,384,16):
                    if round((max(channel_data[j][9:20]) - min(channel_data[j][9:20])) / median_even / 100, 2) == 0.06:
                        output += convert_to_table(j) + "\n"
                        print(convert_to_table(j))#Запись в файл
                        output += str(round((max(channel_data[j][9:20]) - min(channel_data[j][9:20])) / median_even / 100, 2)) + "\n"
                    print(round((max(channel_data[j][9:20]) - min(channel_data[j][9:20])) / median_even / 100, 2))#Запись в файл
                for j in range(i+1, 384, 16):
                    if round((max(channel_data[j][9:20]) - min(channel_data[j][9:20])) / median_non_even / 100,2) == 0.06:
                        output += convert_to_table(j) + "\n"
                        print(convert_to_table(j))#Запись в файл
                        output += str(round((max(channel_data[j][9:20]) - min(channel_data[j][9:20])) / median_even / 100, 2)) + "\n"
                        print(round((max(channel_data[j][9:20]) - min(channel_data[j][9:20])) / median_non_even / 100,2))#Запись в файл
            file = open("cy5_data.txt", "w")
            file.write(output)
            file.close()
        elif channel_name == "hex":
            output = "--------hex-------- \n"
            numerator = 0
            for i in range(len(channel_data)):
                numerator += max(channel_data[i][11:28]) - min(channel_data[i][11:28])
            for i in range(len(channel_data)):
                num = abs(max(channel_data[i][11:28]) - min(channel_data[i][11:28])) / (numerator / len(channel_data))
                if 0.8 <= num <= 1.2:
                    output += f"Measurement {convert_to_table(i + 1)} - {round(abs(max(channel_data[i][11:28]) - min(channel_data[i][11:28])) / (numerator / len(channel_data)), 2)}\n"
            file = open("hex_data.txt", "w")
            file.write(output)
            file.close()
        else:
            print("wrong channel!")

"""extractig file, looking averange, comparing resulst and write to file"""
class Meashurements():
    def __init__(self, path):
        self.path = path
    
    # extracting data from input file
    def extract_data(self, path:str) -> list:
        data = open(self.path).readlines()
        return data
    
    # searching averange value
    def get_averange(self, meashurements:list) -> int:
        averange = 0 
        for i in range(len(meashurements)):
            lst = meashurements[i].split(";")
            averange += int(max(lst[11:28])) - int(min(lst[11:28]))
        return averange
    
    # comparing calculations with averange value
    def compare_results_hex(self, meashurements:list, averange:int) -> str:
        result = ""
        for i in range(len(meashurements)):
            lst = meashurements[i].split(";")
            num = abs((int(max(lst[11:28])) - int(min(lst[11:28]))) / (averange / len(meashurements)))
            if 0.8 <= num <= 1.2:
                result += f"Measurement {i + 1} - {abs((int(max(lst[11:28])) - int(min(lst[11:28]))) / 
                                                       (averange / len(meashurements)))}\n"
        return result
    
    # comparing calculations with averange value
    def compare_results_fam(self, meashurements:list, averange:int) -> str:
        result = ""
        for i in range(len(meashurements)):
            lst = meashurements[i].split(";")
            num = abs((int(max(lst[7:21])) - int(min(lst[7:21]))) / (averange / len(meashurements)))
            if 0.8 <= num <= 1.2:
                result += f"Measurement {i + 1} - {abs((int(max(lst[7:21])) - int(min(lst[7:21]))) / 
                                                       (averange / len(meashurements)))}\n"
        return result
    
    # comparing calculations with averange value
    def compare_results_cy5(self, meashurements:list, averange:int) -> str:
        result = ""
        for i in range(len(meashurements)):
            lst = meashurements[i].split(";")
            num = abs((int(max(lst[9:20])) - int(min(lst[9:20]))) / (averange / len(meashurements)))
            if 0.8 <= num <= 1.2:
                result += f"Measurement {i + 1} - {abs((int(max(lst[9:20])) - int(min(lst[9:20]))) / 
                                                       (averange / len(meashurements)))}\n"
        return result
    
    # writing correct calculations to file "meashurements.txt"
    def write_results_to_file(self, meashurements:str) -> None:
        out_file = open("meashurements.txt", "w")
        out_file.write(meashurements)
        out_file.close()
    
    

# get digit form file and converting to table pin
def convert_to_table(num:int) -> str:
    alphabet = list(string.ascii_uppercase[:16])
    line = 1
    column = alphabet[num % 16]
    return column + str(line + (num // 16))

#get table pin and converting to digit in file
def convert_to_num(num:str) -> int:
    alphabet = list(string.ascii_uppercase[:16])
    dic = {}
    for i in range(len(alphabet)):
        dic.update({alphabet[i]: int(i)})
    return int(dic[num[0]]) + int(num[1:]) * 16 - 16
