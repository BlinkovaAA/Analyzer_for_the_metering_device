import lib
import os

path = input()
basename, extension = os.path.splitext(path)
print(extension)

if extension == ".rt":
    test = lib.rt_action(path)
    #rt_action.protocol_info(test.path)
    chanel_data_fam = lib.rt_action.extract_channel_data(0, test.path) # 0 - Fam; 1 - hex; 2 - Rox; 3 - Cy5; 4 - Cy5.5
    lib.rt_action.search_relationship("fam", chanel_data_fam)
    chanel_data_hex = lib.rt_action.extract_channel_data(1, test.path)
    lib.rt_action.search_relationship("hex", chanel_data_hex)
    chanel_data_hex = lib.rt_action.extract_channel_data(2, test.path)
    lib.rt_action.search_relationship("cy5", chanel_data_hex)
elif extension == ".csv":
    print(0)
else:
    print("wrong file")

#print(chanel_data)
#print(len(chanel_data))
