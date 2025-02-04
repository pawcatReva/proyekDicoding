import streamlit as st 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Load dataset
day_df = pd.read_csv(r"dashboardd\day_cleaned.csv")
hour_df = pd.read_csv(r"dashboardd\hour_cleaned.csv")

# Sidebar Navigasi
with st.sidebar:
    st.title("Bike Sharing Data Set")
    
    selected_page = st.selectbox(
        label="Navigasi",
        options=('Beranda', 'Data Set', 'Pertanyaan 1', 'Pertanyaan 2', 'Pertanyaan 3', 'Pertanyaan 4', 'RFM Analysis', 'Kesimpulan')
    )

# **Tampilkan Konten Berdasarkan Navigasi**
if selected_page == "Beranda":
    st.title("Analisis Data: Bike Sharing Data Set")
    
    st.markdown( """
    **Pertanyaan Bisnis:**  
    1. Bagaimana perbandingan Penggunaan Sepeda pada Hari Libur dan Tidak Libur?
    2. Bagaimana pola penggunaan sepeda pada hari-hari tertentu?  
    3. Bagaimana pola penggunaan sepeda pada musim-musim tertentu?  
    4. Waktu (jam) dengan peminjaman tertinggi berdasarkan jam?
    5. Bagaimana segmentasi peminjaman menggunakan RFM Analysis?
    """)

elif selected_page == "Data Set":
    st.title("Data Set Bike Sharing")
    st.subheader("Day Dataset")
    st.dataframe(day_df.head())
    st.subheader("Deskripsi Data")
    st.write(day_df.describe())

    st.subheader("Hour Dataset")
    st.dataframe(hour_df.head())
    st.subheader("Deskripsi Data")
    st.write(hour_df.describe())

elif selected_page == "Pertanyaan 1":
    st.title("Bagaimana perbandingan Penggunaan Sepeda pada Hari Libur dan Tidak Libur?")
    
    plt.figure(figsize=(10,6))
    sns.boxplot(x='holiday', y='cnt', data=day_df)
    plt.title('Perbandingan Penggunaan Sepeda pada Hari Libur vs Bukan Libur')
    plt.xlabel('Hari Libur (1 = Ya, 0 = Tidak)')
    plt.ylabel('Jumlah Peminjaman Sepeda')
    st.pyplot(plt)
    st.markdown("""
     **1. Bagaimana perbandingan Penggunaan Sepeda pada Hari Libur dan Tidak Libur?**
        - Penggunaan sepeda cenderung lebih rendah pada hari libur, kemungkinan karena banyak orang tidak bepergian ke kantor/sekolah.
        - Sedangkan data menunjukkan data lebih meningkat di hari kerja/biasa dikarenakan aktivitas berjalan di hari kerja/hari biasa.
                """)

elif selected_page == "Pertanyaan 2":
    st.title("Bagaimana pola penggunaan sepeda pada hari-hari tertentu?")
    plt.figure(figsize=(10,6))
    sns.barplot(x='weekday', y='cnt', hue='weekday', data=day_df, palette='viridis', legend=False)
    plt.title('Pola Penggunaan Sepeda Berdasarkan Hari dalam Minggu')
    plt.xlabel('Hari dalam Minggu')
    plt.ylabel('Jumlah Peminjaman Sepeda')
    plt.xticks(ticks=range(7), labels=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
    st.pyplot(plt)
    st.markdown("""
                **2. Bagaimana pola penggunaan sepeda pada hari-hari tertentu?**
       - Penggunaan sepeda lebih tinggi pada hari kerja, kemungkinan besar karena digunakan sebagai transportasi harian saat pergi bekerja/aktivitas.
       - Akhir pekan menunjukkan penurunan, bisa jadi karena banyak orang lebih memilih kendaraan pribadi, aktivitas lain atau hanya diam dirumah/tidak kemana-mana.
                """)

elif selected_page == "Pertanyaan 3":
    st.title("Bagaimana pola penggunaan sepeda pada musim-musim tertentu?")
    plt.figure(figsize=(10,6))
    sns.barplot(x='season', y='cnt', hue='season', data=day_df, palette='Set2', legend=False)
    plt.title('Pola Penggunaan Sepeda Berdasarkan Musim')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Peminjaman Sepeda')
    plt.xticks(ticks=range(4), labels=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
    st.pyplot(plt)
    st.markdown("""
     **3. Bagaimana pola penggunaan sepeda pada musim-musim tertentu?**
    - Cuaca memiliki pengaruh besar terhadap peminjaman sepeda. Musim panas dan gugur adalah periode puncak penggunaan sepeda.
    - Sedangkan musim dingin mengalami penurunan signifikan, dikarenakan suhu cuaca sangat dingin untuk beraktivitas dan jalan tertutup dengan salju (jika turun salju).
                """)

elif selected_page == "Pertanyaan 4":
    st.title("Waktu (jam) dengan peminjaman tertinggi berdasarkan jam?")
    plt.figure(figsize=(12,6))
    sns.histplot(hour_df, x='hr', weights='cnt', bins=24, kde=True, color='blue')
    plt.title("Distribusi Peminjaman Sepeda Berdasarkan Jam", fontsize=14)
    plt.xlabel("Jam (0-23)", fontsize=12)
    plt.ylabel("Jumlah Peminjaman Sepeda", fontsize=12)
    st.pyplot(plt)
    st.markdown("""
        **4. Waktu (jam) dengan peminjaman tertinggi berdasarkan jam?**
       - Dari visualisasi histplot distribusi peminjaman sepeda berdasarkan jam (hour_df), terlihat bahwa peminjaman tertinggi terjadi pada jam sibuk (sekitar pagi dan sore hari).
       - Puncak peminjaman biasanya terjadi pada jam 07:00 - 09:00 pagi (perjalanan ke kantor/sekolah) dan 17:00 - 19:00 sore (perjalanan pulang kerja).
       - Hal ini mengindikasikan bahwa sepeda lebih sering digunakan sebagai alat transportasi harian dibandingkan rekreasi.
                """)

elif selected_page == "RFM Analysis":
    st.title("RFM Analysis pada Peminjaman Sepeda")
    
    # Konversi tanggal
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    latest_date = day_df['dteday'].max()
    
    # Hitung Recency, Frequency, dan Monetary
    rfm_df = day_df.groupby('dteday').agg({
        'cnt': ['sum', 'count']
    }).reset_index()
    
    rfm_df.columns = ['Tanggal', 'Monetary', 'Frequency']
    rfm_df['Recency'] = (latest_date - rfm_df['Tanggal']).dt.days
    
    st.subheader("Hasil RFM Analysis")
    st.dataframe(rfm_df.head())
    
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='Recency', y='Monetary', size='Frequency', sizes=(20, 200), data=rfm_df, alpha=0.7)
    plt.title("Analisis RFM pada Peminjaman Sepeda")
    plt.xlabel("Recency (Hari Sejak Peminjaman Terakhir)")
    plt.ylabel("Total Peminjaman (Monetary)")
    st.pyplot(plt)
    st.markdown("""
    1. **Recency (Seberapa Baru Transaksi Terakhir?)**: Semakin kecil nilai recency, semakin baru seseorang terakhir kali menggunakan layanan peminjaman sepeda.
  Banyak pelanggan yang masih aktif menggunakan layanan secara reguler.
  2. **Frequency (Seberapa Sering Peminjaman Dilakukan?)**: Sebagian besar pengguna hanya meminjam beberapa kali dalam seminggu.
  Ada kelompok pelanggan dengan frekuensi tinggi, kemungkinan pekerja atau pelanggan tetap.
 3. **Monetary (Total Peminjaman yang Dilakukan)**: Pengguna dengan monetary tinggi berarti sering menggunakan layanan sepeda dalam jumlah besar.
  Dari scatterplot, terlihat bahwa pelanggan dengan recency rendah (baru-baru ini meminjam) memiliki monetary yang cukup tinggi.
                """)

elif selected_page == "Kesimpulan":
    st.title("Kesimpulan")
    st.markdown("""
    - **Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan hari libur.**
    - **Hari kerja memiliki tren peminjaman yang lebih tinggi**, kemungkinan karena digunakan sebagai alat transportasi harian.
    - **Musim mempengaruhi jumlah peminjaman sepeda**, dengan penggunaan tertinggi pada musim panas/gugur dan terendah pada musim dingin.
    - **Pola peminjaman sepeda meningkat pada jam sibuk (07:00-09:00 & 17:00-19:00)** yang menunjukkan penggunaan untuk keperluan kerja.
    - **Analisis RFM menunjukkan bahwa sebagian besar peminjaman terjadi baru-baru ini**, dan ada pola penggunaan berulang dari pengguna reguler.
    - **RFM Analysis menunjukkan bahwa sebagian besar pengguna masih aktif,** tetapi ada segmen yang jarang menggunakan layanan ini, yang bisa menjadi target untuk strategi promosi.
    """)