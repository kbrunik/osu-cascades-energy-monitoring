import os
import time
from datetime import datetime
import pandas as pd
#from keys import get_server_key, set_server_key

#pullData function takes in the IP address, username, password, 
# and server number and saves todays file to the current directory
def pullData(FTP_HOST,FTP_USER,FTP_PASS,SERVER_NUM):
    import pysftp as sftp
    #gets todays file name based on date
    now = datetime.now()
    Fdate= now.strftime("%Y%m%d")
    Fname = "Trend_Virtual_Meter_Watt_"+Fdate+"_"+str(SERVER_NUM)+".csv"
    
    #if file already exists, delete it
    if os.path.exists(Fname):
        remove_csv(Fname)

    
    print("Attempting to download"+Fname+" at ")
    print(datetime.now())
    print(time.time())

    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None

    #connect to sftp server and download file
    with sftp.Connection(host=FTP_HOST, username=FTP_USER, password=FTP_PASS, cnopts=cnopts, port=2222) as sftp:
        sftp.chdir('trend')
        sftp.get("Trend_Virtual_Meter_Watt_"+Fdate+".csv")
        print("Download successful")
        os.rename("Trend_Virtual_Meter_Watt_"+Fdate+".csv","Trend_Virtual_Meter_Watt_"+Fdate+"_"+str(SERVER_NUM)+".csv")

def daily_data_trim(ID):
    Fname = file_name(ID)

    df = pd.read_csv(Fname, header = 0)
    remove_csv(Fname)

    # Find number of columns with data
    search_row = df.iloc[1,:].dropna()
    num_col = len(search_row)
    num_meters = int((num_col-2) / 3)

    meters = ['Date', 'Time']

    # Make list to rename column titles
    for i in range(num_meters):
        meters.append("Server" + str(ID) + "_" + "meter" + str(i+1) + "_avg")
        meters.append("Server" + str(ID) + "_" + "meter" + str(i+1) + "_min")
        meters.append("Server" + str(ID) + "_" + "meter" + str(i+1) + "_max")

    # Preparing and saving csv
    df = df.iloc[:,:num_col]
    df.columns = meters
    df.to_csv(Fname, index = False)
    
def fill_master(ID_LIST):
    df_5min_master = pd.DataFrame()

    dfs = [pd.read_csv(os.getcwd() + "/" + file_name(id), index_col=False) for id in ID_LIST]
    df_5min_master = pd.concat(dfs, axis = 1)
    df_5min_master = df_5min_master.loc[:,~df_5min_master.columns.duplicated(keep='first')].copy()
    #df_5min_master = df_5min_master.iloc[-2,:]
    #df_5min_master = df_5min_master.to_frame().T
        
    # Check to see if there are nan values in 5-minute dataframe
    if df_5min_master.isnull().values.any():
        # Wait 20 seconds and try again to collect data
        print("Missing Data...Waiting 20 seconds to try again...")
        time.sleep(20)
        fill_master(ID_LIST)
    
    # absolute value the data in columns titled "Server1_meter10_avg" and "Server1_meter10_min" and "Server1_meter10_max"
    df_5min_master['Server1_meter10_avg'] = df_5min_master['Server1_meter10_avg'].abs()
    df_5min_master['Server1_meter10_min'] = df_5min_master['Server1_meter10_min'].abs()
    df_5min_master['Server1_meter10_max'] = df_5min_master['Server1_meter10_max'].abs()

    #assigns servers to the correct floor. See servermap.xlsx for more details
    df_5min_master['1st_Floor'] = df_5min_master['Server1_meter1_avg'] + df_5min_master['Server3_meter1_avg']
    df_5min_master['2nd_Floor'] = df_5min_master['Server1_meter3_avg'] + df_5min_master['Server1_meter5_avg'] + df_5min_master['Server1_meter10_avg'] + df_5min_master['Server3_meter2_avg']
    df_5min_master['3rd_Floor'] = df_5min_master['Server1_meter4_avg'] + df_5min_master['Server1_meter7_avg'] + df_5min_master['Server1_meter9_avg'] + df_5min_master['Server3_meter4_avg']
    df_5min_master['4th_Floor'] = df_5min_master['Server1_meter6_avg'] + df_5min_master['Server1_meter8_avg'] + df_5min_master['Server1_meter13_avg'] + df_5min_master['Server3_meter3_avg']
    df_5min_master['Utilities'] = df_5min_master['Server1_meter11_avg'] + df_5min_master['Server1_meter12_avg'] + df_5min_master['Server2_meter2_avg'] + df_5min_master['Server2_meter3_avg'] + df_5min_master['Server2_meter5_avg'] + df_5min_master['Server3_meter5_avg'] + df_5min_master['Server3_meter6_avg']
    df_5min_master['TOTAL'] = df_5min_master['1st_Floor'] + df_5min_master['2nd_Floor'] + df_5min_master['3rd_Floor'] + df_5min_master['4th_Floor'] + df_5min_master['Utilities']
    
    
    # calculate the Kwh for each floor and total
    df_5min_master['1st_Floor_Kwh'] = df_5min_master['1st_Floor'] * 5 / 60 / 1000
    df_5min_master['2nd_Floor_Kwh'] = df_5min_master['2nd_Floor'] * 5 / 60 / 1000
    df_5min_master['3rd_Floor_Kwh'] = df_5min_master['3rd_Floor'] * 5 / 60 / 1000
    df_5min_master['4th_Floor_Kwh'] = df_5min_master['4th_Floor'] * 5 / 60 / 1000
    df_5min_master['Utilities_Kwh'] = df_5min_master['Utilities'] * 5 / 60 / 1000
    df_5min_master['TOTAL_Kwh'] = df_5min_master['TOTAL'] * 5 / 60 / 1000

    # May not be needed
    # number of rooms on each floor:
    # first_rooms = 22
    # second_rooms = 49
    # third_rooms = 49
    # fourth_rooms = 35

    # # calculate the Kwh per room for each floor
    # df_5min_master['1st_Floor_Kwh_per_room'] = df_5min_master['1st_Floor_Kwh'] / first_rooms
    # df_5min_master['2nd_Floor_Kwh_per_room'] = df_5min_master['2nd_Floor_Kwh'] / second_rooms
    # df_5min_master['3rd_Floor_Kwh_per_room'] = df_5min_master['3rd_Floor_Kwh'] / third_rooms
    # df_5min_master['4th_Floor_Kwh_per_room'] = df_5min_master['4th_Floor_Kwh'] / fourth_rooms


    return df_5min_master

def pull_5_min_data(ID_LIST):
    df_5min_master = pd.DataFrame()

    dfs = [pd.read_csv(os.getcwd() + "/" + file_name(id), index_col=False) for id in ID_LIST]
    df_5min_master = pd.concat(dfs, axis = 1)
    df_5min_master = df_5min_master.loc[:,~df_5min_master.columns.duplicated(keep='first')].copy()
    df_5min_master = df_5min_master.iloc[-2,:]
    df_5min_master = df_5min_master.to_frame().T
        
    # Check to see if there are nan values in 5-minute dataframe
    if df_5min_master.isnull().values.any():
        # Wait 20 seconds and try again to collect data
        print("Missing Data...Waiting 20 seconds to try again...")
        time.sleep(20)
        pull_5_min_data(ID_LIST)
    
    # absolute value the data in columns titled "Server1_meter10_avg" and "Server1_meter10_min" and "Server1_meter10_max"
    df_5min_master['Server1_meter10_avg'] = df_5min_master['Server1_meter10_avg'].abs()
    df_5min_master['Server1_meter10_min'] = df_5min_master['Server1_meter10_min'].abs()
    df_5min_master['Server1_meter10_max'] = df_5min_master['Server1_meter10_max'].abs()

    #assigns servers to the correct floor. See servermap.xlsx for more details
    df_5min_master['1st_Floor'] = df_5min_master['Server1_meter1_avg'] + df_5min_master['Server3_meter1_avg']
    df_5min_master['2nd_Floor'] = df_5min_master['Server1_meter3_avg'] + df_5min_master['Server1_meter5_avg'] + df_5min_master['Server1_meter10_avg'] + df_5min_master['Server3_meter2_avg']
    df_5min_master['3rd_Floor'] = df_5min_master['Server1_meter4_avg'] + df_5min_master['Server1_meter7_avg'] + df_5min_master['Server1_meter9_avg'] + df_5min_master['Server3_meter4_avg']
    df_5min_master['4th_Floor'] = df_5min_master['Server1_meter6_avg'] + df_5min_master['Server1_meter8_avg'] + df_5min_master['Server1_meter13_avg'] + df_5min_master['Server3_meter3_avg']
    df_5min_master['Utilities'] = df_5min_master['Server1_meter11_avg'] + df_5min_master['Server1_meter12_avg'] + df_5min_master['Server2_meter2_avg'] + df_5min_master['Server2_meter3_avg'] + df_5min_master['Server2_meter5_avg'] + df_5min_master['Server3_meter5_avg'] + df_5min_master['Server3_meter6_avg']
    df_5min_master['TOTAL'] = df_5min_master['1st_Floor'] + df_5min_master['2nd_Floor'] + df_5min_master['3rd_Floor'] + df_5min_master['4th_Floor'] + df_5min_master['Utilities']
    
    
    # calculate the Kwh for each floor and total
    df_5min_master['1st_Floor_Kwh'] = df_5min_master['1st_Floor'] * 5 / 60 / 1000
    df_5min_master['2nd_Floor_Kwh'] = df_5min_master['2nd_Floor'] * 5 / 60 / 1000
    df_5min_master['3rd_Floor_Kwh'] = df_5min_master['3rd_Floor'] * 5 / 60 / 1000
    df_5min_master['4th_Floor_Kwh'] = df_5min_master['4th_Floor'] * 5 / 60 / 1000
    df_5min_master['Utilities_Kwh'] = df_5min_master['Utilities'] * 5 / 60 / 1000
    df_5min_master['TOTAL_Kwh'] = df_5min_master['TOTAL'] * 5 / 60 / 1000

    # May not be needed
    # number of rooms on each floor:
    # first_rooms = 22
    # second_rooms = 49
    # third_rooms = 49
    # fourth_rooms = 35

    # # calculate the Kwh per room for each floor
    # df_5min_master['1st_Floor_Kwh_per_room'] = df_5min_master['1st_Floor_Kwh'] / first_rooms
    # df_5min_master['2nd_Floor_Kwh_per_room'] = df_5min_master['2nd_Floor_Kwh'] / second_rooms
    # df_5min_master['3rd_Floor_Kwh_per_room'] = df_5min_master['3rd_Floor_Kwh'] / third_rooms
    # df_5min_master['4th_Floor_Kwh_per_room'] = df_5min_master['4th_Floor_Kwh'] / fourth_rooms


    return df_5min_master

def merge_master(df_5min_master):
    master = pd.read_csv(os.getcwd() + '\master.csv')
    # Merge 5 minute dataframe with master
    # If time in df_5min_master is not in master, add it to master
    print(df_5min_master['Time'].iloc[0])
    if df_5min_master['Time'].iloc[0] not in master['Time'].iloc[-1]:
        master = pd.concat([master, df_5min_master],ignore_index = False)

    df_5min_master.to_csv(os.getcwd() + '\df_5min_master.csv', index = False)
    master.to_csv(os.getcwd() + '\master.csv', index = False)
    return master, df_5min_master


def file_name(ID):
    now = datetime.now()
    Fdate= now.strftime("%Y%m%d")
    return "Trend_Virtual_Meter_Watt_"+Fdate+"_"+str(ID)+".csv"

def remove_csv(file_name): # removes file from cwd
    path = os.getcwd()+ "\\" + file_name
    if os.path.exists(path):
        os.remove(path)
        print(file_name+' cleared')
    else:
        print(file_name+' cannot be removed. Does it exist?')
    return

# Can be used for testing Raw_Data.py on its own
def main():

    while True:
        SERVER_IDS = [1, 2, 3]
        print("starting data collection...")
        pullData("10.113.1.158","ftp","ftp","1")
        daily_data_trim(1)
        pullData("10.113.1.157","ftp","ftp","2")
        daily_data_trim(2)
        pullData("10.113.1.155","ftp","ftp","3")
        daily_data_trim(3)
        merged_dadta = fill_master(SERVER_IDS)
        #merged_dadta = pull_5_min_data(SERVER_IDS)
        merged_data = merge_master(merged_dadta)
        print("Done!")
        time.sleep(60)

main()