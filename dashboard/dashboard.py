import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import datetime
from babel.numbers import format_currency

def create_daily_rentals_df(df):
    daily_sewa_df = df.resample(rule='D', on='date').agg({
        "total_count_day": "sum"
    })
    daily_sewa_df = daily_sewa_df.reset_index()
    
    return daily_sewa_df

def create_weekday_weekend_df(df):
    weekday_weekend_df = df.groupby(['workingday_day'])['total_count_day'].mean().reset_index()
    return weekday_weekend_df

def create_hour_df(df):
    hour_df = df.groupby(['hour'])['total_count_hour'].mean()
    return hour_df

def create_weather_df(df):
    weather_df = df.groupby(['weather_day'])['total_count_day'].mean().reset_index()
    return weather_df

def create_season_df(df):
    season_df = df.groupby(['season_day'])['total_count_day'].mean().reset_index()
    return season_df
# --------------------------------------------------------------

bike_all_df = pd.read_csv("./Dashboard/bike_all_data.csv") 

# --------------------------------------------------------------

bike_all_df.sort_values(by="date", inplace=True)
bike_all_df.reset_index(inplace=True)
bike_all_df["date"] = pd.to_datetime(bike_all_df["date"])

min_date = bike_all_df["date"].min()
max_date = bike_all_df["date"].max()

with st.sidebar:
    st.header("Bike-Shar")

    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value = min_date,
        max_value=max_date, value=[min_date,max_date]
    )

# ----------------------------------------------------------------
main_df = bike_all_df[(bike_all_df["date"] >= str(start_date)) & 
                (bike_all_df["date"] <= str(end_date))]

daily_rentals_df = create_daily_rentals_df(main_df)
weekday_weekend_df = create_weekday_weekend_df(main_df)
hour_df = create_hour_df(main_df)
weather_df = create_weather_df(main_df)
season_df = create_season_df(main_df)
    

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Daily Bike-Rentals')

total_rentals = daily_rentals_df.total_count_day.sum()
st.metric("Total Rentals", value=total_rentals)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["date"],
    daily_rentals_df["total_count_day"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


st.subheader("Average Bike-Sharing Patterns")


fig, ax= plt.subplots(figsize=(8, 5))
colors = ["#1f77b4", "#ff7f0e"]
sns.barplot(
    x="workingday_day",
    y="total_count_day",
    data=weekday_weekend_df.sort_values(by="total_count_day", ascending=False),
    palette = colors
)
ax.set_title("Average Bike Sharing on Weekdays vs. Weekends", loc="center", fontsize=10)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_xticks(['No', 'Yes'])
ax.set_xticklabels(['Weekends', 'Weekdays'])
st.pyplot(fig)


fig, ax= plt.subplots(figsize=(12, 5))
plt.bar(hour_df.index, hour_df.values, color='#6495ED')
ax.set_title("Average Bike Sharing on Hour", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_xticks(hour_df.index)
st.pyplot(fig)



st.subheader("Season and Weather Effects on Average Bike Sharing Rate")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
sns.barplot(y="weather_day", x="total_count_day", data=weather_df, palette="plasma", ax=ax[0])
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].set_title("Average Bike-Sharing by Weather", loc="center", fontsize=15)

sns.barplot(y="season_day", x="total_count_day", data=season_df, palette="viridis", ax=ax[1])
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].set_title("Average Bike-Sharing by Season", loc="center", fontsize=15)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
st.pyplot(fig)
