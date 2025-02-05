import streamlit as st 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def load_data():
    day_df = pd.read_csv("dashboard/day_cleaned.csv")
    hour_df = pd.read_csv("dashboard/hour_cleaned.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar Navigasi
with st.sidebar:
    st.title("Bike Sharing Data Set")
    selected_page = st.selectbox(
        label="Navigasi",
        options=('Beranda', 'Analisis Data', 'Kesimpulan')
    )

# Halaman Beranda
if selected_page == "Beranda":
    st.title("Analisis Data: Bike Sharing Data Set")
    st.subheader("Dataset Bike Sharing")
    st.subheader("Day")
    st.dataframe(day_df.head())
    st.subheader("Hour")
    st.dataframe(hour_df.head())
    st.subheader("Pertanyaan Bisnis")
    st.markdown("""
    1. Bagaimana perbandingan Penggunaan Sepeda pada Hari Libur dan Tidak Libur?
    2. Bagaimana pola penggunaan sepeda pada hari-hari tertentu?
    3. Bagaimana pola penggunaan sepeda pada musim-musim tertentu?
    4. Waktu (jam) dengan peminjaman tertinggi berdasarkan jam?
    
    **Pendekatan Clustering Manual**
    - Segmentasi pengguna berdasarkan jumlah peminjaman sepeda.
    """)

elif selected_page == "Analisis Data":
    st.title("Analisis Data Bike Sharing")
    
    # Sidebar untuk filtering
    types_of_day = st.sidebar.multiselect("Pilih Hari Libur/Non-Libur:", [0, 1], default=[0, 1], format_func=lambda x: "Hari Libur" if x == 1 else "Hari Biasa")
    seasons = st.sidebar.multiselect("Pilih Musim:", [1, 2, 3, 4], default=[1, 2, 3, 4], format_func=lambda x: ["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"][x-1])
    weather_options = {1: "Cerah", 2: "Berkabut", 3: "Hujan Ringan", 4: "Badai"}
    selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca:", list(weather_options.keys()), default=list(weather_options.keys()), format_func=lambda x: weather_options[x])
    
    day_df_filtered = day_df[(day_df['holiday'].isin(types_of_day)) & (day_df['season'].isin(seasons)) & (day_df['weathersit'].isin(selected_weather))]
    
    question = st.selectbox("Pilih Pertanyaan untuk Analisis:", [
        "Perbandingan Penggunaan Sepeda pada Hari Libur vs Non-Libur",
        "Pola Penggunaan Sepeda Berdasarkan Hari dalam Minggu",
        "Pola Penggunaan Sepeda Berdasarkan Musim",
        "Waktu dengan Peminjaman Tertinggi Berdasarkan Jam"
    ])
    
    if question == "Perbandingan Penggunaan Sepeda pada Hari Libur vs Non-Libur":
        st.subheader("Perbandingan Penggunaan Sepeda pada Hari Libur vs Non-Libur")
        plt.figure(figsize=(10,6))
        sns.boxplot(x='holiday', y='cnt', data=day_df_filtered)
        st.pyplot(plt)
        st.markdown("""
        **Bagaimana perbandingan Penggunaan Sepeda pada Hari Libur dan Tidak Libur?**
        - Penggunaan sepeda cenderung lebih rendah pada hari libur.
        - Penggunaan lebih tinggi pada hari kerja karena aktivitas normal berjalan.
        """)
    
    elif question == "Pola Penggunaan Sepeda Berdasarkan Hari dalam Minggu":
        st.subheader("Pola Penggunaan Sepeda Berdasarkan Hari dalam Minggu")
        plt.figure(figsize=(10,6))
        sns.barplot(x='weekday', y='cnt', hue='weekday', data=day_df_filtered, palette='viridis', legend=False)
        st.pyplot(plt)
        st.markdown("""
        **Bagaimana pola penggunaan sepeda pada hari-hari tertentu?**
        - Penggunaan lebih tinggi pada hari kerja.
        - Akhir pekan menunjukkan penurunan karena alternatif transportasi lain.
        """)
    
    elif question == "Pola Penggunaan Sepeda Berdasarkan Musim":
        st.subheader("Pola Penggunaan Sepeda Berdasarkan Musim")
        plt.figure(figsize=(10,6))
        sns.barplot(x='season', y='cnt', hue='season', data=day_df_filtered, palette='Set2', legend=False)
        st.pyplot(plt)
        st.markdown("""
        **Bagaimana pola penggunaan sepeda pada musim-musim tertentu?**
        - Musim panas dan gugur memiliki peminjaman tertinggi.
        - Musim semi dan musim dingin mengalami penurunan signifikan.
        """)

    elif question == "Waktu dengan Peminjaman Tertinggi Berdasarkan Jam":
        st.subheader("Waktu dengan Peminjaman Tertinggi Berdasarkan Jam")
        plt.figure(figsize=(10,6))
        sns.histplot(hour_df, x='hr', weights='cnt', bins=24, kde=True, color='blue')
        plt.xlabel("Jam")
        plt.ylabel("Jumlah Peminjaman")
        plt.xticks(range(0, 24))  # Menampilkan semua jam (0-23)
        st.pyplot(plt)
        st.markdown("""
        **Waktu (jam) dengan peminjaman tertinggi?**
        - Peminjaman meningkat pada jam sibuk pagi (07:00-09:00) dan sore (17:00-19:00).
        - Ini menunjukkan penggunaan sepeda untuk transportasi kerja atau sekolah.
        - Garis melengkung menunjukkan distribusi peminjaman lebih halus.
        """)
    
    # Clustering Manual untuk Segmentasi Pengguna
    st.subheader("Segmentasi Pengguna Sepeda dengan Clustering Manual")
    
    def categorize_users(cnt):
        if cnt < 1000:
            return "Pengguna Rendah"
        elif 1000 <= cnt < 4000:
            return "Pengguna Sedang"
        else:
            return "Pengguna Tinggi"
    
    day_df_filtered['User Category'] = day_df_filtered['cnt'].apply(categorize_users)
    st.dataframe(day_df_filtered[['dteday', 'cnt', 'User Category']].head())
    
    plt.figure(figsize=(10,6))
    sns.boxplot(x='User Category', y='cnt', data=day_df_filtered, palette='coolwarm')
    st.pyplot(plt)
    st.markdown("""
    **Kesimpulan dari Clustering Manual:**
    - Pengguna sepeda dikelompokkan ke dalam tiga kategori.
    - **Pengguna Rendah**: Meminjam secara sporadis.
    - **Pengguna Sedang**: Cukup rutin menggunakan sepeda.
    - **Pengguna Tinggi**: Sangat sering menggunakan sepeda.
    """)

elif selected_page == "Kesimpulan":
    st.title("Kesimpulan")
    st.markdown("""
    - **Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan hari libur.**
    - **Hari kerja memiliki tren peminjaman lebih tinggi** karena digunakan untuk transportasi harian.
    - **Musim mempengaruhi jumlah peminjaman sepeda**, dengan peminjaman tertinggi pada musim panas/gugur.
    - **Peminjaman meningkat pada jam sibuk (07:00-09:00 & 17:00-19:00)** menunjukkan penggunaan untuk bekerja.
    - **Segmentasi pengguna membantu memahami pola penggunaan dan strategi promosi.**
    """)
