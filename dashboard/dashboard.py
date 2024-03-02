import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset
day_df = pd.read_csv("dashboard/main.csv")

# Streamlit app
st.title("Kring-kring, Inilah Dashboard Rental Sepeda🚲")
st.write(
    "Selamat datang di Dashboard Rental Sepeda! 🌟 Dashboard ini dirancang untuk memberikan wawasan mendalam tentang tren penggunaan rental sepeda. "
    "Dengan berbagai grafik dan statistik, kita akan menjelajahi bagaimana sepeda dipinjamkan dari waktu ke waktu. Ayo kita mulai petualangan kita! 🚀"
)

with st.container():
  st.header("Tren Penggunaan Rental Sepeda")
  st.write("Tampilan grafik dibawah ini merupakan treen penggunaan sepeda selama bulan/kuartal/tahun loh,"
           "Lihat grafik di bawah ini untuk mendapatkan wawasan yang mendalam. Jangan lupa eksplorasi menu di bawah ini ya! 🚀")
  col1,col2 = st.columns([1,1])
  with col1:
    option = st.selectbox("Pilih Grafik", ["Bulan", "Kuartal", "Tahun"])

# Convert datetime column to datetime format
datetime_columns = ["dteday"]
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

# Create monthly subset
monthly = day_df[((day_df['yr'] == 0) & (day_df['mnth'] <= 12)) | ((day_df['yr'] == 1) & (day_df['mnth'] <= 12))]
unique_years = monthly['dteday'].dt.year.unique()
year_mapping = dict(zip([0, 1], unique_years))
monthly['yr'] = monthly['yr'].map(year_mapping)

max_temp = 41
max_atemp = 50

monthly['original_temp'] = day_df['temp'] * max_temp
monthly['original_atemp'] = day_df['atemp'] * max_atemp

monthly['quarter'] = pd.cut(monthly['mnth'], bins=[0, 3, 6, 9, 12], labels=['Q1', 'Q2', 'Q3', 'Q4'])
monthly['quarter_year'] = monthly['yr'].astype(str) + "-" + monthly['quarter'].astype(str)

# Function to create bar chart based on selected option
def create_bar_chart(data, x, y, color, xlabel, ylabel, title):
    plt.figure(figsize=(12, 6))
    bars = plt.bar(data[x], data[y], color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

    return plt

# Function to create statistical graph with temperature information
def create_statistical_graph(plot_data, temp_data, atemp_data):
    plt.figure(figsize=(12, 6))
    ax1 = sns.lineplot(x='quarter_year', y='cnt', data=plot_data, marker='o', color='coral', markersize=8, label='Count/Q')
    plt.title('Total Penggunaan Sepeda dan Rata-Rata Suhu pada Tahun-Kuartal')
    plt.xlabel('Tahun-Kuartal')
    plt.ylabel('Jumlah Penggunaan Sepeda')

    ax2 = ax1.twinx()
    sns.lineplot(x='quarter_year', y='original_temp', data=temp_data, marker='s', color='forestgreen', markersize=8,
                 ax=ax2, label='Temp/Q')
    sns.lineplot(x='quarter_year', y='original_atemp', data=atemp_data, marker='s', color='limegreen', markersize=8,
                 ax=ax2, label='ATemp/Q')
    ax2.set_ylabel('Suhu(°C)')

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='best')

    return plt


# Process data based on selected option
if option == "Bulan":
    # Year selection for the monthly chart
    with col2:
      selected_year_month = st.selectbox("Pilih Tahun", unique_years)
    data_to_plot = monthly[(monthly['yr'] == selected_year_month)].groupby(['mnth'])['cnt'].sum().reset_index()
    data_to_plot.columns = ['Month', 'Total_Count']
    chart = create_bar_chart(data_to_plot, 'Month', 'Total_Count', color='skyblue',
                              xlabel='Bulan', ylabel='Jumlah Penggunaan Sepeda', title='Jumlah Penggunaan Sepeda/Bulan')
    st.pyplot(chart)

elif option == "Kuartal":
    # Year selection for the quarterly chart
    with col2:
      selected_year_quarter = st.selectbox("Pilih Tahun", unique_years)
    monthly['quarter'] = pd.cut(monthly['mnth'], bins=[0, 3, 6, 9, 12], labels=['Q1', 'Q2', 'Q3', 'Q4'])
    data_to_plot = monthly[(monthly['yr'] == selected_year_quarter)].groupby(['quarter'])['cnt'].sum().reset_index()
    data_to_plot.columns = ['Quarter', 'Total_Count']
    chart = create_bar_chart(data_to_plot, 'Quarter', 'Total_Count', color='lightgreen',
                              xlabel='Kuartal', ylabel='Jumlah Penggunaan Sepeda', title='Jumlah Penggunaan Sepeda/Kuartal')
    st.pyplot(chart)

elif option == "Tahun":
    data_to_plot = day_df.groupby(day_df['dteday'].dt.year)['cnt'].sum().reset_index()
    data_to_plot.columns = ['Year', 'Total_Count']
    chart = create_bar_chart(data_to_plot, 'Year', 'Total_Count', color='salmon',
                              xlabel='Tahun', ylabel='Jumlah Penggunaan Sepeda', title='Jumlah Penggunaan Sepeda/Tahun')
    st.pyplot(chart)

st.markdown("---")

with st.container():
  st.header("Pengaruh Suhu dan Penggunaan Rental Sepeda")
  st.write(
        "Mari kita telusuri hubungan antara suhu dan penggunaan rental sepeda.🌡️ "
        "Grafik di bawah ini menampilkan seberapa besar suhu mempengaruhi jumlah sepeda yang dipinjamkan. "
        "Ayo lihat apa yang dapat kita temukan!"
    )
# Statistical graph
temp_data = monthly.groupby('quarter_year')['original_temp'].mean().reset_index()
atemp_data = monthly.groupby('quarter_year')['original_atemp'].mean().reset_index()
plot_data = monthly.groupby('quarter_year')['cnt'].sum().reset_index()

statistical_chart = create_statistical_graph(plot_data, temp_data, atemp_data)
st.pyplot(statistical_chart)
