import pandas as pd

import matplotlib.pyplot as plt

import streamlit as st



# ==========================

# KONFIGURASI HALAMAN WEB STREAMLIT

# ==========================

st.set_page_config(page_title="Eco-Forest KPHP Lalan", layout="wide")



# Header Utama & Logo

st.title("🌳 ECO-FOREST KPHP LALAN MANGSANG MENDIS")

st.image("logo unisba.jpg", width=150)

st.markdown("**Sistem Informasi Geografis & Analisis Finansial Hasil Hutan Berkelanjutan**")

st.write("---")
# ==========================================
# 2. DATA STATIS BASE (DARI DOKUMEN & KODE ANDA)
# ==========================================
forest_profile = {
    "forest_area_ha": 259940,
    "production_forest_block_ha": 166164.92,
    "hhbk_block_ha": 34675.90,
    "community_block_ha": 59099.18
}

wood_production = {
    "annual_volume_m3": 440000,
    "projected_volume_10yr_m3": 500000,
    "wood_price_rp_m3": 1618000
}

hhbk_production = {
    "jelutung_kg": 697796,
    "karet_kg": 3241005,
    "nipah_liter": 325000,
    "nanas_buah": 42000,
    "ikan_kg": 58150
}

# Data Rencana Aksi Restorasi Lapangan (Dokumen Rencana Aksi)
data_restorasi = {
    'Lokus Wilayah': [
        'HP Lalan (Desa Trans Lampung)', 
        'HP Lalan (Desa Muara Medak)', 
        'HP Mangsang (Desa Suka Damai)', 
        'Blok Jasa Lingkungan (Gambut)'
    ],
    'Estimasi Luas (Ha)': [1000, 1000, 500, 500],
    'Komoditas Utama': ['Kenaf (Serat Alam)', 'Nilam (Minyak Atsiri)', 'Sengon + Singkong', 'Pohon Jelutung'],
    'Pola Pengembangan': ['Tumpang Sari / Monokultur', 'Pengayaan Spesies', 'Agroforestri', 'Pengayaan Spesies Lokal']
}
df_restorasi = pd.DataFrame(data_restorasi)

# Data Kelayakan Finansial Proyek Investasi Restorasi (Discount Rate 5%)
data_kelayakan_proyek = {
    'Komoditas Proyek': [
        'Getah Jelutung (100 Ha)', 
        'Serat Alam Kenaf (100 Ha)', 
        'Agroforestri Sengon & Singkong (100 Ha)', 
        'Minyak Nilam (20 Ha)', 
        'Persemaian Mandiri / Nursery (2 Ha)'
    ],
    'NPV (Rupiah)': [41664172746, 4557258660, 3165145633, 2672971229, 376725634],
    'IRR (%)': [13, 15, 10, 19, 20],
    'BCR': [1.71, 1.41, 1.21, 1.16, 1.55]
}
df_kelayakan = pd.DataFrame(data_kelayakan_proyek)

# ==========================================
# 3. FITUR INTERAKTIF: SIDEBAR (KONTROL HARGA)
# ==========================================
st.sidebar.header("⚙️ Pengaturan Simulasi Harga Pasar")
st.sidebar.markdown("Geser slider untuk melihat proyeksi dampak harga makro terhadap pendapatan tahunan kawasan:")

price_wood = st.sidebar.slider("Harga Kayu (Rp/m³)", 1000000, 2500000, 1618000, step=50000)
price_jelutung = st.sidebar.slider("Harga Jelutung (Rp/kg)", 50000, 150000, 90000, step=5000)
price_karet = st.sidebar.slider("Harga Karet (Rp/kg)", 10000, 40000, 20000, step=1000)
price_nipah = st.sidebar.slider("Harga Nipah (Rp/Liter)", 2000, 10000, 5000, step=500)
price_nanas = st.sidebar.slider("Harga Nanas (Rp/Buah)", 1000, 8000, 3000, step=500)
price_ikan = st.sidebar.slider("Harga Ikan (Rp/kg)", 15000, 60000, 30000, step=2000)

# ==========================================
# 4. PERHITUNGAN PENDAPATAN MAKRO DINAMIS
# ==========================================
wood_income = wood_production["annual_volume_m3"] * price_wood
jelutung_income = hhbk_production["jelutung_kg"] * price_jelutung
karet_income = hhbk_production["karet_kg"] * price_karet
nipah_income = hhbk_production["nipah_liter"] * price_nipah
nanas_income = hhbk_production["nanas_buah"] * price_nanas
ikan_income = hhbk_production["ikan_kg"] * price_ikan

total_income = wood_income + jelutung_income + karet_income + nipah_income + nanas_income + ikan_income
total_income_miliar = total_income / 1_000_000_000

# Pembuatan Dataframe Produksi Aktual Makro
df_makro = pd.DataFrame({
    "Komoditas": ["Kayu", "Jelutung", "Karet", "Nipah", "Nanas", "Ikan"],
    "Volume Produksi": [
        wood_production["annual_volume_m3"],
        hhbk_production["jelutung_kg"],
        hhbk_production["karet_kg"],
        hhbk_production["nipah_liter"],
        hhbk_production["nanas_buah"],
        hhbk_production["ikan_kg"]
    ],
    "Satuan": ["m³", "Kg", "Kg", "Liter", "Buah", "Kg"],
    "Harga Simulasi": [price_wood, price_jelutung, price_karet, price_nipah, price_nanas, price_ikan],
    "Total Pendapatan": [wood_income, jelutung_income, karet_income, nipah_income, nanas_income, ikan_income]
})

# ==========================================
# 5. LAYOUT UTAMA MENGGUNAKAN TABS (4 TABS)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Ringkasan Eksekutif", 
    "📋 Tabel Data Makro", 
    "📈 Grafik Visualisasi Lahan & Makro",
    "🌱 Rencana Aksi Restorasi & Investasi Mikro"
])

# --- TAB 1: RINGKASAN EKSEKUTIF ---
with tab1:
    st.subheader("📌 Indikator Capaian Utama KPHP Lalan")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Luas Kawasan Hutan", value=f"{forest_profile['forest_area_ha']:,} Ha".replace(",", "."))
    with col2:
        st.metric(label="Rata-rata Produksi Kayu / Tahun", value=f"{wood_production['annual_volume_m3']:,} m³".replace(",", "."))
    with col3:
        st.metric(label="Total Estimasi Pendapatan Makro", value=f"Rp {total_income_miliar:.2f} Miliar/Tahun")
        
    st.write("---")
    
    st.markdown("""
    ### 📝 Keterangan Karakteristik Wilayah Kerja & Profil Organisasi
    **KPHP Lalan Mangsang Mendis** berlokasi di wilayah Kabupaten Musi Banyuasin, Provinsi Sumatera Selatan. Kawasan ini memiliki karakteristik ekosistem yang unik karena didominasi oleh lahan basah dan **hutan rawa gambut** terdegradasi akibat kebakaran hutan historis.
    
    Berdasarkan studi implementasi kebijakan, unit pengelola tapak dibentuk berdasarkan **Peraturan Bupati No. 24 Tahun 2009** dengan status awal sebagai **UPTD**. Pengelolaan wilayah menitikberatkan pada keseimbangan ekonomi-ekologi melalui pembagian tiga blok ruang:
    * **Blok Produksi**: Dioptimalkan untuk pemanfaatan komoditas kayu industri secara berkelanjutan.
    * **Blok HHBK (Hasil Hutan Bukan Kayu)**: Difokuskan pada komoditas bernilai tinggi ramah lingkungan seperti getah Jelutung dan karet.
    * **Blok Pemberdayaan (Community)**: Melibatkan masyarakat lokal untuk pengelolaan komoditas pangan agroforestri dan kemitraan lingkungan.
    
    *Catatan Analisis Struktur Organisasi:* KPH menghadapi tantangan keterbatasan SDM operasional (hanya 5 personil) dan kesesuaian latar belakang teknis kehutanan struktural yang minim, sehingga memerlukan penguatan kapasitas kelembagaan menuju **SKPD Mandiri / Lembaga Lain** sesuai Pasal 45 PP No. 41 Tahun 2007.
    """)

# --- TAB 2: TABEL DATA MAKRO ---
with tab2:
    st.subheader("📋 Matriks Produksi dan Nilai Ekonomi Komoditas Wilayah Kerja")
    st.markdown("Berikut adalah rincian data kuantitatif tahunan hasil simulasi harga pasar:")
    
    st.dataframe(df_makro.style.format({
        "Volume Produksi": "{:,.0f}",
        "Harga Simulasi": "Rp {:,.0f}",
        "Total Pendapatan": "Rp {:,.0f}"
    }), use_container_width=True)
    
    st.write("---")
    
    csv_data = df_makro.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Tabel Data Makro (.CSV)",
        data=csv_data,
        file_name="Data_Ekonomi_KPHP_Lalan_Makro.csv",
        mime="text/csv"
    )

# --- TAB 3: GRAFIK VISUALISASI LAHAN & MAKRO ---
with tab3:
    st.subheader("📈 Analisis Proporsi Lahan dan Kontribusi Sektoral Makro")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Grafik Batang Kontribusi Pendapatan (Matplotlib)
        fig1, ax1 = plt.subplots(figsize=(6, 5))
        colors_bar = ['#008080' if x == 'Kayu' else '#4682B4' for x in df_makro["Komoditas"]]
        ax1.bar(df_makro["Komoditas"], df_makro["Total Pendapatan"] / 1_000_000_000, color=colors_bar)
        ax1.set_title("Kontribusi Pendapatan Finansial Makro (Miliar Rp)", fontsize=11, fontweight='bold')
        ax1.set_ylabel("Miliar Rupiah")
        ax1.set_xlabel("Komoditas")
        st.pyplot(fig1)
        st.caption("Batang hijau tua menunjukkan komoditas Kayu sebagai tulang punggung pendapatan utama kawasan.")
        
    with col_chart2:
        # Grafik Lingkaran Alokasi Lahan Kawasan (Matplotlib)
        labels_lahan = ["Blok Produksi", "Blok HHBK", "Blok Pemberdayaan"]
        sizes_lahan = [
            forest_profile["production_forest_block_ha"],
            forest_profile["hhbk_block_ha"],
            forest_profile["community_block_ha"]
        ]
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        ax2.pie(sizes_lahan, labels=labels_lahan, autopct="%1.1f%%", startangle=140, colors=["#2ca02c", "#ff7f0e", "#1f77b4"])
        ax2.set_title("Persentase Pembagian Alokasi Ruang KPHP", fontsize=11, fontweight='bold')
        st.pyplot(fig2)
        st.caption("Tata guna lahan makro KPHP didominasi oleh Blok Produksi komoditas kayu.")

# --- TAB 4: RENCANA AKSI RESTORASI & INVESTASI MIKRO (PENYATUAN DATA DOKUMEN) ---
with tab4:
    st.subheader("🌱 Strategi Pemulihan Kawasan Bekas Kebakaran (Diagnosa & Rencana Restorasi)")
    st.markdown("""
    Melalui kolaborasi multipihak (*ICRAF, WRI Indonesia, KLHK, dan NGO*), KPHP Lalan Mangsang Mendis telah menyusun zonasi prioritas restorasi lahan kritis akibat kebakaran hutan berulang. 
    Program pemulihan lahan ini diintegrasikan langsung dengan peningkatan ekonomi masyarakat sekitar zona tapak melalui skema **Kemitraan Kehutanan dan Perhutanan Sosial**.
    """)
    
    col_res1, col_res2 = st.columns([4, 3])
    
    with col_res1:
        st.markdown("**Matriks Sebaran Geografis Lokus Restorasi**")
        st.dataframe(df_restorasi, use_container_width=True)
    
    with col_res2:
        st.markdown("**Proporsi Target Luasan Restorasi per Lokus**")
        fig_pie_res = px.pie(
            df_restorasi, 
            values='Estimasi Luas (Ha)', 
            names='Lokus Wilayah', 
            hole=0.3,
            color_discrete_sequence=px.colors.sequential.Plotly3
        )
        st.plotly_chart(fig_pie_res, use_container_width=True)
        
    st.write("---")
    
    st.subheader("💰 Hasil Analisis Investasi & Kelayakan Finansial Komoditas Mikro")
    st.markdown("Parameter kelayakan usaha komoditas HHBK restorasi dihitung dengan asumsi suku bunga acuan (*Discount Rate*) sebesar **5%**:")
    
    # Menampilkan Tabel Analisis Finansial Gabungan
    st.dataframe(df_kelayakan.style.format({
        'NPV (Rupiah)': 'Rp {:,.0f}',
        'IRR (%)': '{:.0f}%',
        'BCR': '{:.2f}'
    }), use_container_width=True)
    
    col_bar_res1, col_bar_res2 = st.columns(2)
    
    with col_bar_res1:
        # Grafik Analisis Nilai Bersih Sekarang (NPV Proyek) dengan Plotly
        st.markdown("**Perbandingan Nilai NPV Usaha Restorasi (Rupiah)**")
        fig_plotly_npv = px.bar(
            df_kelayakan.sort_values(by='NPV (Rupiah)', ascending=True),
            x='NPV (Rupiah)',
            y='Komoditas Proyek',
            orientation='h',
            text_auto='.3s',
            color='NPV (Rupiah)',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_plotly_npv, use_container_width=True)
        
    with col_bar_res2:
        # Grafik Analisis Rasio Keuntungan Efisiensi Biaya (BCR Proyek) dengan Plotly
        st.markdown("**Perbandingan Nilai Rasio Keuntungan (Benefit-Cost Ratio / BCR)**")
        fig_plotly_bcr = px.bar(
            df_kelayakan.sort_values(by='BCR', ascending=True),
            x='BCR',
            y='Komoditas Proyek',
            orientation='h',
            text_auto=True,
            color='BCR',
            color_continuous_scale='Plasma'
        )
        st.plotly_chart(fig_plotly_bcr, use_container_width=True)
        
    st.info("""
    💡 **Rangkuman Eksekutif Kelayakan Finansial:**
    * **Komoditas Getah Jelutung (Paludikultur Gambut)** menghasilkan keuntungan finansial tertinggi dengan NPV mencapai **Rp 41,6 Miliar** per 100 Ha.
    * **Pembangunan Persemaian Mandiri (Nursery 2 Ha)** dan **Minyak Nilam** memiliki laju pengembalian modal tercepat dengan persentase **IRR masing-masing 20% dan 19%**.
    * Seluruh jenis pilihan komoditas restorasi dinilai **Sangat Layak secara Finansial** karena memiliki parameter **BCR > 1.0**.
    """)