import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
 
######################################################################

# LOAD DATA
# sale_data = pd.read_pickle('sale_data.pkl')
# rent_data = pd.read_pickle('rent_data.pkl')


# FOR SALE FILES
sale_files = [
    'sale_data_hist_1.pkl',
    'sale_data_hist_2.pkl',
    'sale_data_hist_3.pkl',
    'sale_data_hist_4.pkl',
    'sale_data.pkl'
]

sale_dfs = [pd.read_pickle(file) for file in sale_files]
sale_data = pd.concat(sale_dfs, ignore_index=True)



# FOR RENT FILES
rent_files = [
    'rent_data_hist_1.pkl',
    'rent_data.pkl'
]

rent_dfs = [pd.read_pickle(file) for file in rent_files]
rent_data = pd.concat(rent_dfs, ignore_index=True)


######################################################################
### DEFINE FILTER RANGES
# max_floors = int(sale_data['floor'].max())
# max_rooms = int(sale_data['rooms'].max())
# max_size = int(sale_data['square_m'].max())
max_floors = int(23)
max_rooms = int(6)
max_size = int(250)


######################################################################
### SIDEBAR ###
### REGION SELECTION
regions = sale_data['region'].value_counts().index.values
regions = np.insert(regions, 0, 'All regions')

select_region = st.sidebar.selectbox('Select region:', regions)

if select_region != 'All regions':
    sale_data = sale_data[sale_data['region'] == select_region]
    rent_data = rent_data[rent_data['region'] == select_region]
    
    
### FLOOR SELECTION
select_floor = st.sidebar.slider('Select floor:', value=[1, max_floors], min_value = 1, max_value = max_floors)

### ROOM COUNT SELECTION
select_rooms = st.sidebar.slider('Select room count:', value=[1, max_rooms], min_value = 1, max_value = max_rooms)

### SIZE SELECTION
select_size = st.sidebar.slider('Select size (square meters):', value=[1, max_size], min_value = 1, max_value = max_size)

### DATA FILTERING
sale_data = sale_data[
    (sale_data['floor'] >= select_floor[0]) &
    (sale_data['floor'] <= select_floor[1]) &
    (sale_data['rooms'] >= select_rooms[0]) &
    (sale_data['rooms'] <= select_rooms[1]) &
    (sale_data['square_m'] >= select_size[0]) &
    (sale_data['square_m'] <= select_size[1])
]

rent_data = rent_data[
    (rent_data['floor'] >= select_floor[0]) &
    (rent_data['floor'] <= select_floor[1]) &
    (rent_data['rooms'] >= select_rooms[0]) &
    (rent_data['rooms'] <= select_rooms[1]) &
    (rent_data['square_m'] >= select_size[0]) &
    (rent_data['square_m'] <= select_size[1])
]


######################################################################
### CREATE SUMMARY TABLE
sale_summary = sale_data.groupby('time')
sale_summary = sale_summary.agg(
                                count = ('rooms', 'count'),
                                median_price_per_square = ('price_per_square_m', 'median')
                                )

rent_summary = rent_data.groupby('time')
rent_summary = rent_summary.agg(
                                count = ('rooms', 'count'),
                                median_price_per_square = ('price_per_square_m', 'median')
                                )


######################################################################
### TABS ###
# sale_tab, rent_tab = st.tabs(['FOR SALE', 'FOR RENT'])
sale_tab, rent_tab, yields_tab, about_tab = st.tabs(['FOR SALE', 'FOR RENT', 'YIELDS', 'ABOUT THE APP'])
# sale_tab, rent_tab, about_tab = st.tabs(['FOR SALE', 'FOR RENT', 'ABOUT THE APP'])

######################################################################
### FOR SALE TAB ###
sale_tab.header('Apartments for sale')
# sale_tab.caption('On the sidebar at the left, you can specify the criteria by which you want to filter the data. All charts and tables in all the tabs are automatically updated right after the filter setting is changed. Once per day, at around midnight, the dataset is updated with the latest advertisement data.')
sale_tab.caption('')

### CHARTS
sale_tab.subheader('Number of Active Listings')
sale_tab.caption('Below chart shows how many apartments were listed for sale at particular dates')
fig_sale_count = px.line(sale_summary, y='count')
sale_tab.plotly_chart(fig_sale_count, theme="streamlit")

sale_tab.subheader('Median price per square meter')
sale_tab.caption('Below chart shows the median price per square meter at particular dates')
fig_sale_price = px.line(sale_summary, y='median_price_per_square', labels={'median_price_per_square':'median price per square meter'})
sale_tab.plotly_chart(fig_sale_price, theme="streamlit")


######################################################################
### FOR RENT TAB ###
rent_tab.header('Apartments for rent')
# rent_tab.caption('On the sidebar at the left, you can specify the criteria by which you want to filter the data. All charts and tables in all the tabs are automatically updated right after the filter setting is changed. Once per day, at around midnight, the dataset is updated with the latest advertisement data.')
rent_tab.caption('')

### CHARTS
rent_tab.subheader('Number of Active Listings')
rent_tab.caption('Below chart shows how many apartments were listed for rent at particular dates')
fig_rent_count = px.line(rent_summary, y='count')
rent_tab.plotly_chart(fig_rent_count, theme="streamlit")

rent_tab.subheader('Median price per square meter')
rent_tab.caption('Below chart shows the median price per square meter at particular dates')
fig_rent_price = px.line(rent_summary, y='median_price_per_square', labels={'median_price_per_square':'median price per square meter'})
rent_tab.plotly_chart(fig_rent_price, theme="streamlit")


######################################################################
# ### YIELDS TAB ###

yield_annual = ((rent_summary['median_price_per_square'] * 12) / sale_summary['median_price_per_square']) * 100

# ### CHARTS
yields_tab.subheader('Annual yield')
yields_tab.caption('Below chart shows the annual yield of renting out an apartment, according to median rent and sale price per square meter. The formula is:')
yields_tab.caption('(median rent price per square meter * 12)  /  median sale price per square meter')

fig_yield = px.line(yield_annual, y='median_price_per_square', labels={'median_price_per_square':'annual yield (%)'})
yields_tab.plotly_chart(fig_yield, theme="streamlit")


######################################################################
### ABOUT THE APP TAB ###
about_tab.header('About the app')
about_tab.caption('This app provides a summarized overview of apartment listings posted on the website ss.lv. It allows users to view the number of apartment advertisements active at the end of each day, as well as the median price per square meter for these listings.')
about_tab.caption('You can toggle between apartments for sale and for rent, and the data displayed in the charts can be customized using the filters on the left-hand sidebar. These filters allow you to narrow down the listings by specific city regions, apartment size, room count, and floor.')
about_tab.caption('New information is added at the end of each day.')
