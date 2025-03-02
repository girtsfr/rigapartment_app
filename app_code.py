import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
 
######################################################################
# LOAD DATA (unchanged)
sale_files = [
    'sale_data_hist_1.pkl',
    'sale_data_hist_2.pkl',
    'sale_data_hist_3.pkl',
    'sale_data_hist_4.pkl',
    'sale_data.pkl'
]
sale_dfs = [pd.read_pickle(file) for file in sale_files]
sale_data = pd.concat(sale_dfs, ignore_index=True)

rent_files = [
    'rent_data_hist_1.pkl',
    'rent_data.pkl'
]
rent_dfs = [pd.read_pickle(file) for file in rent_files]
rent_data = pd.concat(rent_dfs, ignore_index=True)

######################################################################
# DEFINE FILTER RANGES (unchanged)
max_floors = int(23)
max_rooms = int(6)
max_size = int(250)

######################################################################
# SIDEBAR (unchanged)
regions = sale_data['region'].value_counts().index.values
regions = np.insert(regions, 0, 'All regions')
select_region = st.sidebar.selectbox('Select region:', regions)

if select_region != 'All regions':
    sale_data = sale_data[sale_data['region'] == select_region]
    rent_data = rent_data[rent_data['region'] == select_region]
    
select_floor = st.sidebar.slider('Select floor:', value=[1, max_floors], min_value=1, max_value=max_floors)
select_rooms = st.sidebar.slider('Select room count:', value=[1, max_rooms], min_value=1, max_value=max_rooms)
select_size = st.sidebar.slider('Select size (square meters):', value=[1, max_size], min_value=1, max_value=max_size)

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
# CREATE SUMMARY TABLE WITH YOY CHANGES
sale_data['time'] = pd.to_datetime(sale_data['time'])
rent_data['time'] = pd.to_datetime(rent_data['time'])

# Sale summary with YoY
sale_summary = sale_data.groupby('time').agg(
    count=('rooms', 'count'),
    median_price_per_square=('price_per_square_m', 'median')
)
sale_summary['count_yoy'] = sale_summary['count'].pct_change(periods=365) * 100
sale_summary['price_yoy'] = sale_summary['median_price_per_square'].pct_change(periods=365) * 100

# Rent summary with YoY
rent_summary = rent_data.groupby('time').agg(
    count=('rooms', 'count'),
    median_price_per_square=('price_per_square_m', 'median')
)
rent_summary['count_yoy'] = rent_summary['count'].pct_change(periods=365) * 100
rent_summary['price_yoy'] = rent_summary['median_price_per_square'].pct_change(periods=365) * 100

######################################################################
# TABS (unchanged)
sale_tab, rent_tab, yields_tab, about_tab = st.tabs(['FOR SALE', 'FOR RENT', 'YIELDS', 'ABOUT THE APP'])

######################################################################
# FOR SALE TAB
with sale_tab:
    st.header('Apartments for sale')
    st.caption('')

    # Number of Active Listings
    st.subheader('Number of Active Listings')
    st.caption('Below chart shows how many apartments were listed for sale at particular dates')
    fig_sale_count = px.line(sale_summary, y='count')
    st.plotly_chart(fig_sale_count, theme="streamlit")

    # YoY Change in Number of Listings
    st.subheader('Year-over-Year Change in Number of Listings')
    st.caption('Below chart shows the YoY percentage change in number of sale listings')
    fig_sale_count_yoy = px.line(sale_summary, y='count_yoy', 
                                labels={'count_yoy': 'YoY % Change'},
                                title='YoY % Change in Listings Count')
    st.plotly_chart(fig_sale_count_yoy, theme="streamlit")

    # Median price per square meter
    st.subheader('Median Price per Square Meter')
    st.caption('Below chart shows the median price per square meter at particular dates')
    fig_sale_price = px.line(sale_summary, y='median_price_per_square', 
                           labels={'median_price_per_square': 'median price per square meter'})
    st.plotly_chart(fig_sale_price, theme="streamlit")

    # YoY Change in Price
    st.subheader('Year-over-Year Change in Price per Square Meter')
    st.caption('Below chart shows the YoY percentage change in median sale price per square meter')
    fig_sale_price_yoy = px.line(sale_summary, y='price_yoy',
                                labels={'price_yoy': 'YoY % Change'},
                                title='YoY % Change in Median Price')
    st.plotly_chart(fig_sale_price_yoy, theme="streamlit")

######################################################################
# FOR RENT TAB
with rent_tab:
    st.header('Apartments for rent')
    st.caption('')

    # Number of Active Listings
    st.subheader('Number of Active Listings')
    st.caption('Below chart shows how many apartments were listed for rent at particular dates')
    fig_rent_count = px.line(rent_summary, y='count')
    st.plotly_chart(fig_rent_count, theme="streamlit")

    # YoY Change in Number of Listings
    st.subheader('Year-over-Year Change in Number of Listings')
    st.caption('Below chart shows the YoY percentage change in number of rent listings')
    fig_rent_count_yoy = px.line(rent_summary, y='count_yoy',
                                labels={'count_yoy': 'YoY % Change'},
                                title='YoY % Change in Listings Count')
    st.plotly_chart(fig_rent_count_yoy, theme="streamlit")

    # Median price per square meter
    st.subheader('Median Price per Square Meter')
    st.caption('Below chart shows the median price per square meter at particular dates')
    fig_rent_price = px.line(rent_summary, y='median_price_per_square',
                           labels={'median_price_per_square': 'median price per square meter'})
    st.plotly_chart(fig_rent_price, theme="streamlit")

    # YoY Change in Price
    st.subheader('Year-over-Year Change in Price per Square Meter')
    st.caption('Below chart shows the YoY percentage change in median rent price per square meter')
    fig_rent_price_yoy = px.line(rent_summary, y='price_yoy',
                                labels={'price_yoy': 'YoY % Change'},
                                title='YoY % Change in Median Price')
    st.plotly_chart(fig_rent_price_yoy, theme="streamlit")

######################################################################
# YIELDS TAB
with yields_tab:
    yield_annual = ((rent_summary['median_price_per_square'] * 12) / sale_summary['median_price_per_square']) * 100
    yield_annual = pd.DataFrame(yield_annual, columns=['yield'])
    yield_annual['yield_yoy'] = yield_annual['yield'].pct_change(periods=365) * 100

    st.subheader('Annual Yield')
    st.caption('Below chart shows the annual yield of renting out an apartment')
    fig_yield = px.line(yield_annual, y='yield',
                       labels={'yield': 'annual yield (%)'})
    st.plotly_chart(fig_yield, theme="streamlit")

    st.subheader('Year-over-Year Change in Annual Yield')
    st.caption('Below chart shows the YoY percentage change in annual yield')
    fig_yield_yoy = px.line(yield_annual, y='yield_yoy',
                           labels={'yield_yoy': 'YoY % Change'},
                           title='YoY % Change in Annual Yield')
    st.plotly_chart(fig_yield_yoy, theme="streamlit")

######################################################################
# ABOUT THE APP TAB (unchanged)
with about_tab:
    st.header('About the app')
    st.caption('This app provides a summarized overview of apartment listings posted on the website ss.lv. It allows users to view the number of apartment advertisements active at the end of each day, as well as the median price per square meter for these listings.')
    st.caption('You can toggle between apartments for sale and for rent, and the data displayed in the charts can be customized using the filters on the left-hand sidebar. These filters allow you to narrow down the listings by specific city regions, apartment size, room count, and floor.')
    st.caption('New information is added at the end of each day.')
