import streamlit as st
import numpy as np
import pandas as pd

# Read in data from csv to dataframe
dataframe = pd.read_csv('updated_master.csv',parse_dates=[['Date', 'time']])

dataframe['Time'] = dataframe['Date_time']
print(dataframe.info())
print(dataframe.head())
# Title webpage
st.markdown("<h1 style='text-align: center; color: orange;'>OSU-Cascades Energy Challenge</h1>",
                 unsafe_allow_html=True)
# st.title('ENERGY!!! :zap:')

st.markdown("<h2 style='text-align: center;'>Current Electrical Usage</h2>",
                 unsafe_allow_html=True)
st.write('Current Power Usage')

# Columns with current energy trends
col1, col2, col3, col4, col5 = st.columns(5)    #Establishes number of columns

# Total power consumption averages 
# TODO: Update averages with dynamic updates from dynamic csv
#create variable total_pwr_avg to equal the sum of the column titled Total KWh


total_pwr_avg = dataframe['Total kWh'].sum()
total_pwr_avg = round(total_pwr_avg)

#Avg Kwh per day
#create a variable for each floor to equal the sum of the column titled Avg kWh 1st, Avg kWh 2nd, etc.
flr_1_kWh_Avg = dataframe['Avg kWh 1st'].sum()
flr_1_kWh_Avg = round(flr_1_kWh_Avg)
flr_2_kWh_Avg = dataframe['Avg kWh 2nd'].sum()
flr_2_kWh_Avg = round(flr_2_kWh_Avg)
flr_3_kWh_Avg = dataframe['Avg kWh 3rd'].sum()
flr_3_kWh_Avg = round(flr_3_kWh_Avg)
flr_4_kWh_Avg = dataframe['Avg kWh 4th'].sum()
flr_4_kWh_Avg = round(flr_4_kWh_Avg)
utilities_kWh_Avg = dataframe['Utilites kWh'].sum()
utilities_kWh_Avg = round(utilities_kWh_Avg)
total_kWh_Avg = dataframe['Total kWh'].sum()
total_kWh_Avg = round(total_kWh_Avg)

#Avg kWh per room per day
#create a variable for each floor to equal the sum of the column titled Avg Rm 1st, Avg Rm 2nd, etc.
flr_1_kWh_Rm = dataframe['Avg Rm 1st'].sum()
flr_1_kWh_Rm = round(flr_1_kWh_Rm,2)
flr_2_kWh_Rm = dataframe['Avg Rm 2nd'].sum()
flr_2_kWh_Rm = round(flr_2_kWh_Rm,2)
flr_3_kWh_Rm = dataframe['Avg Rm 3rd'].sum()
flr_3_kWh_Rm = round(flr_3_kWh_Rm,2)
flr_4_kWh_Rm = dataframe['Avg Rm 4th'].sum()
flr_4_kWh_Rm = round(flr_4_kWh_Rm,2)


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
    col1.metric('1st Floor Daily Average','{} kWh'.format(flr_1_kWh_Avg))
    col2.metric('2nd Floor Daily Average','{} kWh'.format(flr_2_kWh_Avg))
    col3.metric('3rd Floor Daily Average','{} kWh'.format(flr_3_kWh_Avg))
    col4.metric('4th Floor Daily Average','{} kWh'.format(flr_4_kWh_Avg))
    with st.expander('See more stats'):
        st.subheader('Average Daily kWh consumption Per Room')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('1st Floor','{} kWh'.format(flr_1_kWh_Rm))
        col2.metric('2nd Floor','{} kWh'.format(flr_2_kWh_Rm))
        col3.metric('3rd Floor','{} kWh'.format(flr_3_kWh_Rm))
        col4.metric('4th Floor','{} kWh'.format(flr_4_kWh_Rm))
    st.line_chart(dataframe,x = 'Time', y = ('1st Floor', '2nd floor','3rd floor','4th floor'))


with tab2:
    st.header('1st Floor')
    st.subheader('The 1st floor consumes :blue['+str(flr_1_kWh_Avg)+' kWh] per day on average! That is equivalent to :blue['+str(flr_1_kWh_Rm)+' kWh] per room per day!')
    st.line_chart(dataframe, x = 'Time', y = ('1st Floor'))

with tab3:
    st.header('2nd Floor')
    st.subheader('The 2nd floor consumes :blue['+str(flr_2_kWh_Avg)+' kWh] per day on average! That is equivalent to :blue['+str(flr_2_kWh_Rm)+' kWh] per room per day!')
    st.line_chart(dataframe, x = 'Time', y = ('2nd floor'))

with tab4:
    st.header('3rd Floor')
    st.subheader('The 3rd floor consumes :blue['+str(flr_3_kWh_Avg)+' kWh] per day on average! That is equivalent to :blue['+str(flr_3_kWh_Rm)+' kWh] per room per day!')
    st.line_chart(dataframe, x = 'Time', y = ('3rd floor'))

with tab5:
    st.header('4th Floor')
    st.subheader('The 4th floor consumes :blue['+str(flr_4_kWh_Avg)+' kWh] per day on average! That is equivalent to :blue['+str(flr_4_kWh_Rm)+' kWh] per room per day!')
    st.line_chart(dataframe, x = 'Time', y = ('4th floor'))

with tab6:
    st.header('Utilities')
    st.subheader('The utilities consume :blue['+str(utilities_kWh_Avg)+' kWh] per day on average!')
    st.line_chart(dataframe, x = 'Time', y = ('Utilities'))
