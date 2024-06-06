import streamlit as st
import pandas as pd
import numpy as np

# Import DataFrames
sessions = pd.read_csv("20240605 - Active Children Sessions-Grid view.csv")
sessions['1min Assessment Score'] = pd.to_numeric(sessions['1min Assessment Score'], errors='coerce')
sessions['Total Sessions'] = pd.to_numeric(sessions['Total Sessions'], errors='coerce')

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
st.info('This gives an indication of current implementation levels. It allows us to compare schools that started late. All schools should have been operating at full capacity in May.')

col3, col4 = st.columns(2)
with col3:
    st.subheader('Sessions per Mentor (May)')
    st.dataframe(data=may_sessions_per_school,width=500,height=300)

with col4:
    st.subheader('Sessions per School (May)')
    st.dataframe(data=may_mentor_sessions, width=500, height=300)

# Variance of Sessions
st.subheader('Session Variance')
st.warning("High variance is bad, it generally means mentors/coaches aren't ensuring all children are receiving a similar number of sessions.")
primary_variance = primary.groupby('Mentor')['Total Sessions'].std().round(1).sort_values(ascending=False)
st.dataframe(data=primary_variance, width=500, height=300)

# Percent of Children with Low Sessions
few_sessions = primary[primary['Total Sessions'] <= 10]
few_sessions_count = few_sessions.groupby('Mentor')['Mcode'].count().reset_index()
few_sessions_count.columns = ['Mentor', 'Children with Low Sessions']
total_sessions_count = primary.groupby('Mentor')['Mcode'].count().reset_index()
total_sessions_count.columns = ['Mentor', 'Total Children']
merged_counts = pd.merge(few_sessions_count, total_sessions_count, on='Mentor')
merged_counts['Percentage'] = (merged_counts['Children with Low Sessions'] / merged_counts['Total Children']).round(3) * 100
low_sessions = merged_counts.sort_values(by='Percentage', ascending=False)

st.subheader('% of Children with Low Sessions')
st.dataframe(data=low_sessions, width=500, height=300)

st.markdown('---')

###### ECD RESULTS #########
st.header('ECDC Results')

st.header('ECDCs Mar - May')

st.subheader('Letter Score')
st.dataframe(data=ecd_letter_score, width=1200, height=500)

col5, col6 = st.columns(2)

with col5:
    st.subheader('Sessions per Mentor')
    st.dataframe(data=ecd_mentor_sessions,width=500,height=215)

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
    st.dataframe(data=ecd_may_sessions_per_school,width=500,height=215)

with col8:
    st.subheader('Sessions per School (May)')
    st.dataframe(data=ecd_may_mentor_sessions, width=500, height=300)

st.subheader('Session Variance')
st.warning("High variance is bad, it generally means mentors/coaches aren't ensuring all children are receiving a similar number of sessions.")
ecd_variance = ecd.groupby('Mentor')['Total Sessions'].std().round(1).sort_values(ascending=False)
st.dataframe(data=ecd_variance, width=500, height=215)
