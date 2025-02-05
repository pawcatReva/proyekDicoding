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
    **1. Perbandingan Penggunaan Sepeda pada Hari Libur dan Tidak Libur.**
    - Hari Kerja (Tidak Libur): Penggunaan sepeda lebih tinggi pada hari kerja. Sepeda digunakan sebagai alat transportasi utama untuk perjalanan menuju tempat kerja, dengan volume peminjaman yang cenderung lebih tinggi.
    - Hari Libur: Pada hari libur, jumlah peminjaman cenderung lebih rendah. Ini mungkin karena banyak orang memilih untuk beristirahat di rumah atau menggunakan moda transportasi lain saat berlibur.\n
    **2. Pola Penggunaan Sepeda pada Hari-Hari Tertentu**
    - Pada hari kerja, terutama di jam-jam sibuk pagi (07:00-09:00) dan sore (17:00-19:00), peminjaman sepeda cenderung tinggi karena banyak orang menggunakannya untuk perjalanan ke dan dari tempat kerja.
    - Pada hari libur, penggunaan sepeda cenderung lebih terdistribusi sepanjang hari tanpa puncak penggunaan yang signifikan. Pengguna lebih cenderung menggunakan sepeda untuk kegiatan santai, berolahraga, atau berwisata.\n
    **3.Pola Penggunaan Sepeda pada Musim-Musim Tertentu.**
    - Musim Panas dan Gugur: Jumlah peminjaman sepeda paling tinggi selama musim panas dan gugur, di mana cuaca cenderung lebih bersahabat untuk bersepeda. Musim ini mendukung aktivitas luar ruangan, sehingga orang lebih cenderung memilih sepeda.
    - Musim Semi dan Dingin: Pada musim semi (Spring) yang cenderung lebih sejuk atau cuaca dingin pada waktu tertentu, 
      peminjaman sepeda dapat menurun karena cuaca yang tidak selalu nyaman untuk bersepeda. Pada cuaca dingin atau hujan, orang lebih memilih menggunakan transportasi tertutup atau memilih untuk tetap di rumah.\n
    **4. Waktu (Jam) dengan Peminjaman Tertinggi Berdasarkan Jam**
    - Peminjaman sepeda mencapai puncaknya pada jam sibuk antara pukul 07:00-09:00 dan 17:00-19:00. Ini menunjukkan pola penggunaan sepeda yang terkait langsung dengan perjalanan menuju dan pulang dari tempat kerja atau aktivitas rutin lainnya.\n
    **Segmentasi Pengguna Sepeda dengan Clustering Manual**
    - Segmentasi pengguna sepeda didasarkan pada jumlah peminjaman yang dapat disesuaikan menggunakan filter di dashboard. Filter ini memungkinkan untuk memilih rentang jumlah peminjaman tertentu, yang secara otomatis membagi pengguna menjadi kategori:
      - Pengguna Rendah: Peminjaman sepeda di bawah nilai yang ditentukan (misalnya < 1.000 peminjaman).
      - Pengguna Sedang: Peminjaman sepeda dalam rentang tertentu (misalnya antara 1.000 hingga 4.000 peminjaman).
      - Pengguna Tinggi: Peminjaman sepeda di atas nilai yang ditentukan (misalnya > 4.500 peminjaman).
    """)
