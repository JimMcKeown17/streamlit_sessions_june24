import streamlit as st
import pandas as pd
import numpy as np

# Import DataFrames
sessions = pd.read_csv("20240605 - Active Children Sessions-Grid view.csv")
sessions['1min Assessment Score'] = pd.to_numeric(sessions['1min Assessment Score'], errors='coerce')

primary = sessions[sessions['Grade'] != "PreR"]
ecd = sessions[sessions['Grade'] == "PreR"]

# Primary Dataframe Calculations
mentor_sessions = primary.groupby('Mentor')['Total Sessions'].mean().round(1).sort_values(ascending=False).to_frame()
sessions_per_school = primary.groupby(['School', 'Mentor'])['Total Sessions'].mean().round(1).sort_values(ascending=False).to_frame()
may_mentor_sessions = primary.groupby(['School', 'Mentor'])['May Total Sessions'].mean().round(1).sort_values(ascending=False).to_frame()
may_sessions_per_school = primary.groupby('Mentor')['May Total Sessions'].mean().round(1).sort_values(ascending=False).to_frame()
display_all_months = primary.groupby(['School', 'Mentor']).agg(
    Mar_Sessions=('Jan - March Total Sessions', 'mean'),
    Apr_Sessions=('April Total Sessions', 'mean'),
    May_Sessions=('May Total Sessions', 'mean'),
    Total_Sessions=('Total Sessions', 'mean')
).round(1).sort_values(by='Total_Sessions', ascending=False)

# ECD Dataframe Calculations
ecd_mentor_sessions = ecd.groupby('Mentor')['Total Sessions'].mean().round(1).sort_values(ascending=False).to_frame()
ecd_sessions_per_school = ecd.groupby(['School', 'Mentor'])['Total Sessions'].mean().round(1).sort_values(ascending=False).to_frame()
ecd_may_mentor_sessions = ecd.groupby(['School', 'Mentor'])['May Total Sessions'].mean().round(1).sort_values(ascending=False).to_frame()
ecd_may_sessions_per_school = ecd.groupby('Mentor')['May Total Sessions'].mean().round(1).sort_values(ascending=False).to_frame()
ecd_display_all_months = ecd.groupby(['School', 'Mentor']).agg(
    Mar_Sessions=('Jan - March Total Sessions', 'mean'),
    Apr_Sessions=('April Total Sessions', 'mean'),
    May_Sessions=('May Total Sessions', 'mean'),
    Total_Sessions=('Total Sessions', 'mean')
).round(1).sort_values(by='Total_Sessions', ascending=False)

ecd_letter_score = ecd.groupby(['School', 'Mentor']).agg(
    Mar_Sessions=('Jan - March Total Sessions', 'mean'),
    Apr_Sessions=('April Total Sessions', 'mean'),
    May_Sessions=('May Total Sessions', 'mean'),
    Total_Sessions=('Total Sessions', 'mean'),
    Letter_Score=('1min Assessment Score', 'mean')
).round(1).sort_values(by='Letter_Score', ascending=False)


# Sections to Display
st.title('Masi Literacy Session Analysis')

st.header('Primary School Results')

col1, col2 = st.columns(2)

with col1:
    st.subheader('Sessions per Mentor')
    st.dataframe(data=mentor_sessions,width=500,height=300)

with col2:
    st.subheader('Sessions per School')
    st.dataframe(data=sessions_per_school, width=500, height=300)

st.subheader('Sessions per Month')
st.dataframe(data=display_all_months, width=1200, height=350)

st.header('Primary Schools Most Recent Month')
st.text('This gives an indication of current implementation stats. Allows us to compare schools that started late.')

col3, col4 = st.columns(2)
with col3:
    st.subheader('Sessions per Mentor (May)')
    st.dataframe(data=may_sessions_per_school,width=500,height=300)

with col4:
    st.subheader('Sessions per School (May)')
    st.dataframe(data=may_mentor_sessions, width=500, height=300)

st.header('ECDC Results')

st.header('ECDCs Mar - May')

st.subheader('Letter Score')
st.dataframe(data=ecd_letter_score, width=1200, height=500)

col5, col6 = st.columns(2)

with col5:
    st.subheader('Sessions per Mentor')
    st.dataframe(data=ecd_mentor_sessions,width=500,height=200)

with col6:
    st.subheader('Sessions per ECD')
    st.dataframe(data=ecd_sessions_per_school, width=500, height=300)

st.subheader('Sessions per Month')
st.dataframe(data=ecd_display_all_months, width=1200, height=350)

st.header('ECDCs Most Recent Month')
st.text('This gives an indication of current implementation stats. Allows us to compare schools that started late.')

col7, col8 = st.columns(2)
with col7:
    st.subheader('Sessions per Mentor (May)')
    st.dataframe(data=ecd_may_sessions_per_school,width=500,height=300)

with col8:
    st.subheader('Sessions per School (May)')
    st.dataframe(data=ecd_may_mentor_sessions, width=500, height=300)

