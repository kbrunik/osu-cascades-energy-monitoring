import streamlit as st
import numpy as np
import pandas as pd
# from Raw_Data import *
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    layout="wide",
)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

#refreshes page every 5 minutes
st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")


# Read in data from csv to dataframe
dataframe = pd.read_csv('master.csv',parse_dates=[['Date', 'Time']])

dataframe['Time'] = dataframe['Date_Time']
print(dataframe.info())
print(dataframe.head())
# Title webpage
st.markdown("<h1 style='text-align: center; color: orange;'>OSU-Cascades Energy Challenge</h1>",unsafe_allow_html=True)
# st.title('ENERGY!!! :zap:')

st.markdown("<h2 style='text-align: center;'>Current Electrical Usage</h2>", unsafe_allow_html=True)
#st.write('Current Power Usage')

# Columns with current energy trends
col1, col2, col3, col4, col5 = st.columns(5)    #Establishes number of columns

#calculate average power usage for each floor
total_pwr_avg = dataframe['TOTAL_Kwh'].sum()
total_pwr_avg = round(total_pwr_avg)
#calculate how many days of data have been collected based on the number of rows in the dataframe
days_of_data = dataframe['TOTAL_Kwh'].count()/288

#calculate kWh per day
#create a variable for each floor to equal the sum of the 1st_Floor_Kwh, 2nd_Floor_Kwh, etc. divided by the number of days of data that have been collected so far
flr_1_kWh_Day = dataframe['1st_Floor_Kwh'].sum()/days_of_data
flr_1_kWh_Day = round(flr_1_kWh_Day,2)
flr_2_kWh_Day = dataframe['2nd_Floor_Kwh'].sum()/days_of_data
flr_2_kWh_Day = round(flr_2_kWh_Day,2)
flr_3_kWh_Day = dataframe['3rd_Floor_Kwh'].sum()/days_of_data
flr_3_kWh_Day = round(flr_3_kWh_Day,2)
flr_4_kWh_Day = dataframe['4th_Floor_Kwh'].sum()/days_of_data
flr_4_kWh_Day = round(flr_4_kWh_Day,2)
utilities_kWh_Day = dataframe['Utilities_Kwh'].sum()/days_of_data
utilities_kWh_Day = round(utilities_kWh_Day,2)





#calculate kWh per room per day
#number of rooms on each floor:
first_rooms = 22
second_rooms = 49
third_rooms = 49
fourth_rooms = 35

#create a variable for each floor to equal the flr1_kWh_Day divided by the number of rooms on that floor
flr_1_kWh_Room_Day = flr_1_kWh_Day/first_rooms
flr_1_kWh_Room_Day = round(flr_1_kWh_Room_Day,2)
flr_2_kWh_Room_Day = flr_2_kWh_Day/second_rooms
flr_2_kWh_Room_Day = round(flr_2_kWh_Room_Day,2)
flr_3_kWh_Room_Day = flr_3_kWh_Day/third_rooms
flr_3_kWh_Room_Day = round(flr_3_kWh_Room_Day,2)
flr_4_kWh_Room_Day = flr_4_kWh_Day/fourth_rooms
flr_4_kWh_Room_Day = round(flr_4_kWh_Room_Day,2)





# Change between last interval and new
# delta_total_avg = 10
# delta_flr_1_avg = 17
# delta_flr_2_avg = 0
# delta_flr_3_avg = -15
# delta_flr_4_avg = 15
# delta_flr_5_avg = 35

# col1.metric('Total Power Usage', 
#              '{} kW'.format(total_pwr_avg), 
#              '{}'.format(delta_total_avg), 
#              delta_color = 'inverse')        #delta_color inverse changes positive values to red
# col2.metric('Floor 1 Power Usage',
#              '{} kW'.format(flr_1_pwr_avg), 
#              '{}'.format(delta_flr_1_avg),
#              delta_color = 'inverse')
# col3.metric('Floor 2 Power Usage', 
#              '{} kW'.format(flr_2_pwr_avg),
#              '{}'.format(delta_flr_2_avg), 
#              delta_color = 'inverse')
# col4.metric('Floor 2 Power Usage', 
#              '{} kW'.format(flr_3_pwr_avg),
#              '{}'.format(delta_flr_3_avg), 
#              delta_color = 'inverse')
# col5.metric('Floor 2 Power Usage', 
#              '{} kW'.format(flr_4_pwr_avg),
#              '{}'.format(delta_flr_4_avg), 
#              delta_color = 'inverse')



tab1, tab7, tab2, tab3, tab4, tab5, tab6,  =    st.tabs(['Total Energy', 'Compare by Floor', 'Floor 1', 'Floor 2', 'Floor 3', 'Floor 4', 'Utilities'])
with tab1:
    st.header('Total Energy Consumption')
    st.metric('Building Daily Average','{} kWh'.format(total_pwr_avg))
    st.line_chart(dataframe, x='Time', y=('TOTAL'))


with tab7:
    st.header('Usage by Floor Comparison')
    col1,col2,col3,col4 = st.columns(4)
    col1.metric('1st Floor Daily Average','{} kWh'.format(flr_1_kWh_Day))
    col2.metric('2nd Floor Daily Average','{} kWh'.format(flr_2_kWh_Day))
    col3.metric('3rd Floor Daily Average','{} kWh'.format(flr_3_kWh_Day))
    col4.metric('4th Floor Daily Average','{} kWh'.format(flr_4_kWh_Day))
    with st.expander('See more stats'):
        st.subheader('Average Daily kWh Consumption Per Room')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('1st Floor','{} kWh'.format(flr_1_kWh_Room_Day))
        col2.metric('2nd Floor','{} kWh'.format(flr_2_kWh_Room_Day))
        col3.metric('3rd Floor','{} kWh'.format(flr_3_kWh_Room_Day))
        col4.metric('4th Floor','{} kWh'.format(flr_4_kWh_Room_Day))
    st.line_chart(dataframe,x = 'Time', y = ('1st_Floor', '2nd_Floor','3rd_Floor','4th_Floor'))


with tab2:
    st.header('1st Floor')
    st.subheader('The 1st floor consumes :blue['+str(flr_1_kWh_Day)+' kWh] per day on average! That is equivalent to :blue['+str(flr_1_kWh_Room_Day)+' kWh] per room per day!')
    st.line_chart(dataframe, x = 'Time', y = ('1st_Floor'))

with tab3:
    st.header('2nd Floor')
    st.subheader('The 2nd floor consumes :blue['+str(flr_2_kWh_Day)+' kWh] per day on average! That is equivalent to :blue['+str(flr_2_kWh_Room_Day)+' kWh] per room per day!')
    st.line_chart(dataframe, x = 'Time', y = ('2nd_Floor'))

with tab4:
    st.header('3rd Floor')
    st.subheader('The 3rd floor consumes :blue['+str(flr_3_kWh_Day)+' kWh] per day on average! That is equivalent to :blue['+str(flr_3_kWh_Room_Day)+' kWh] per room per day!')
    st.line_chart(dataframe, x = 'Time', y = ('3rd_Floor'))

with tab5:
    st.header('4th Floor')
    st.subheader('The 4th floor consumes :blue['+str(flr_4_kWh_Day)+' kWh] per day on average! That is equivalent to :blue['+str(flr_4_kWh_Room_Day)+' kWh] per room per day!')
    st.line_chart(dataframe, x = 'Time', y = ('4th_Floor'))

with tab6:
    st.header('Utilities')
    st.subheader('The utilities consume :blue['+str(utilities_kWh_Day)+' kWh] per day on average!')
    st.line_chart(dataframe, x = 'Time', y = ('Utilities'))