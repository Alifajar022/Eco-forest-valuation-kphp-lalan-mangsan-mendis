import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

# ==========================================
# 1. KONFIGURASI HALAMAN WEB STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Eco-Forest KPHP Lalan", 
    layout="wide",
    page_icon="🌳"
)

# ==========================================
# 2. DATA STATIS BASE (KPHP LALAN)
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
# 3. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("logo unisba.jpg", use_container_width=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Eco-Forest Valuation</h3>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="Navigasi",
        options=["Beranda", "TEV & Trade-off", "Profil Hutan", "Produksi Makro", "Rencana Aksi & Investasi"],
        icons=["house", "book", "tree", "currency-dollar", "graph-up-arrow"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px!", "background-color": "transparent"},
            "icon": {"color": "#E53935", "font-size": "16px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#333333"},
            "nav-link-selected": {"background-color": "#212121"},
        }
    )
    
    st.write("---")
    st.header("⚙️ Parameter Simulasi")
    price_wood = st.slider("Harga Kayu (Rp/m³)", 1000000, 2500000, 1618000, step=50000)
    price_jelutung = st.slider("Harga Jelutung (Rp/kg)", 50000, 150000, 90000, step=5000)
    price_karet = st.slider("Harga Karet (Rp/kg)", 10000, 40000, 20000, step=1000)

    st.write("---")
    st.subheader("🌳 Parameter Ekologi (TEV)")
    carbon_value_ha = st.slider("Nilai Karbon (Rp/Ha/Thn)", 500000, 5000000, 2000000, step=100000)
    water_service_ha = st.slider("Nilai Tata Air (Rp/Ha/Thn)", 100000, 2000000, 1000000, step=50000)
    biodiversity_value_ha = st.slider("Nilai Biodiversitas (Rp/Ha/Thn)", 100000, 3000000, 1500000, step=50000)
    production_intensity = st.slider("Intensitas Eksploitasi (%)", 0, 100, 100, step=5)


# ==========================================
# 4. OPERASI HITUNG DATA (INTEGRASI TEV & TRADE-OFF)
# ==========================================
# Hitung Sektor Ekonomi Produksi Tradisional
wood_income = wood_production["annual_volume_m3"] * price_wood * (production_intensity / 100)
jelutung_income = hhbk_production["jelutung_kg"] * price_jelutung
karet_income = hhbk_production["karet_kg"] * price_karet
total_ekonomi_langsung = wood_income + jelutung_income + karet_income

# Hitung Sektor Ekologi Lingkungan (Terpengaruh oleh Intensitas Eksploitasi/Trade-off)
# Jika Intensitas Eksploitasi Kayu 100%, Fungsi Ekologis menurun hingga sisa 30%
ekologi_multiplier = 1.0 - (0.7 * (production_intensity / 100))
total_luas = forest_profile["forest_area_ha"]

carbon_total = (total_luas * carbon_value_ha) * ekologi_multiplier
water_total = (total_luas * water_service_ha) * ekologi_multiplier
biodiversity_total = (total_luas * biodiversity_value_ha) * ekologi_multiplier
total_ekologi_tidak_langsung = carbon_total + water_total + biodiversity_total

total_income_miliar = total_ekonomi_langsung / 1_000_000_000

df_makro = pd.DataFrame({
    "Komoditas": ["Kayu (Sesuai Intensitas)", "Jelutung", "Karet"],
    "Volume Produksi Base": [wood_production["annual_volume_m3"], hhbk_production["jelutung_kg"], hhbk_production["karet_kg"]],
    "Satuan": ["m³", "Kg", "Kg"],
    "Harga Simulasi": [price_wood, price_jelutung, price_karet],
    "Total Pendapatan (Rp)": [wood_income, jelutung_income, karet_income]
})


# ==========================================
# 5. KONDISIONAL HALAMAN (KONTEN UTAMA)
# ==========================================

# --- HALAMAN 1: BERANDA ---
if selected == "Beranda":
    st.title("🌳 Eco-Forest Valuation KPHP Lalan Mangsang Mendis")
    st.write("PBL 6 — Ekonomi Sumber Daya Hutan")
    st.write("---")
    
    st.header("📚 Informasi Akademik")
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.write("**Mata Kuliah:**")
        st.write("Ekonomi Sumber Daya Alam dan Lingkungan")
    with col_info2:
        st.write("**Dosen Pengampu:**")
        st.write("Yuhka Sundaya, S.E., M.Si.")
    
    st.write("")
    st.markdown("""
    <div style="background-color: #112E14; padding: 18px; border-radius: 8px; color: #81C784; border-left: 6px solid #2E7D32;">
        <b style="color: #FFFFFF; font-size: 16px;">KELOMPOK 1</b><br>
        <span style="color: #FFFFFF;">• Ali Fajar Maulana (10090222056) 
                azrial rafsanzanni (10090222067)</span>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.header("📄 Pendahuluan")
    st.markdown("""
    Kesatuan Pengelolaan Hutan Produksi (KPHP) Lalan Mangsang Mendis merupakan salah satu kawasan 
    hutan strategis di Provinsi Sumatera Selatan yang memiliki peran ganda yang sangat krusial, 
    baik sebagai benteng ekologis (penyerap karbon dan penyeimbang tata air lahan basah/gambut) 
    maupun sebagai penggerak roda ekonomi daerah melalui pemanfaatan hasil hutan.
    
    Namun, sebagian kawasan ini menghadapi tantangan degradasi lahan akibat 
    perubahan fungsi guna tanah dan kebakaran hutan. Oleh karena itu, diperlukan suatu pendekatan 
    **Penilaian Ekonomi Sumber Daya Hutan (Eco-Forest Valuation)** untuk menghitung potensi nyata kawasan. 
    Melalui instrumen dashboard ini, saya mensimulasikan nilai ekonomi makro dari komoditas unggulan 
    seperti kayu, getah jelutung, dan karet, sekaligus memetakan rencana aksi restorasi vegetasi 
    serta uji kelayakan finansial proyek mikro secara terintegrasi dan berkelanjutan.
    """)

# --- HALAMAN NEW SUB MENU: TEV & TRADE-OFF INTERAKTIF ---
elif selected == "TEV & Trade-off":
    st.title("💡 Analisis Komparatif TEV & Efek Trade-off")
    st.write("---")
    
    # Live Analisis Grafik Batang Perbandingan Trade-off Ekonomi vs Ekologi
    st.subheader("📊 Grafik Efek Trade-off Real-Time")
    df_chart = pd.DataFrame({
        "Sektor Nilai (TEV)": ["Manfaat Pasar (Ekonomi Langsung)", "Manfaat Non-Pasar (Ekologi Jasa Lingkungan)"],
        "Nilai Valuasi (Miliar Rp)": [total_ekonomi_langsung/1_000_000_000, total_ekologi_tidak_langsung/1_000_000_000]
    })
    fig_trade = px.bar(df_chart, x="Sektor Nilai (TEV)", y="Nilai Valuasi (Miliar Rp)", color="Sektor Nilai (TEV)",
                       color_discrete_sequence=["#E53935", "#2E7D32"], text_auto='.2f')
    st.plotly_chart(fig_trade, use_container_width=True)
    
    st.write("---")
    
    # Penjelasan Teoretis Pendukung Akurasi Akademis
    col_tev, col_trade = st.columns(2)
    with col_tev:
        st.subheader("1. Komponen Total Economic Value (TEV)")
        st.markdown(f"""
        * **Direct Use Value (Nilai Guna Langsung):** Diperoleh dari ekstraksi fisik komoditas pasar saat ini. Berdasarkan parameter geser Anda, akumulasinya mencapai **Rp {total_ekonomi_langsung/1_000_000_000:,.2f} Miliar**.
        * **Indirect Use Value (Nilai Guna Tidak Langsung):** Berasal dari fungsi regulasi iklim, hidrologi gambut, dan keanekaragaman hayati yang nilainya mencapai **Rp {total_ekologi_tidak_langsung/1_000_000_000:,.2f} Miliar**.
        """)
    with col_trade:
        st.subheader("2. Implikasi Kebijakan Trade-off")
        st.markdown(f"""
        Ketika **Intensitas Eksploitasi** dinaikkan mendekati 100%, keuntungan finansial kayu melonjak tajam dalam jangka pendek. 
        Namun, *trade-off* ekologis yang harus dibayar adalah rusaknya kapasitas *carbon sink* dan runtuhnya ekosistem rawa gambut. 
        Dashboard ini mendemonstrasikan bagaimana pembatasan kuota tebang mampu menyelamatkan nilai ekologi jasa lingkungan jangka panjang.
        """)

# --- HALAMAN 3: PROFIL HUTAN ---
elif selected == "Profil Hutan":
    st.title("📋 Profil Wilayah Kerja KPHP Lalan")
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        ### Pembagian Alokasi Ruang Kawasan:
        * **Total Luas Kawasan:** {forest_profile['forest_area_ha']:,} Ha
        * **Blok Produksi:** {forest_profile['production_forest_block_ha']:,} Ha
        * **Blok HHBK:** {forest_profile['hhbk_block_ha']:,} Ha
        * **Blok Pemberdayaan Masy.:** {forest_profile['community_block_ha']:,} Ha
        """.replace(",", "."))
    with col2:
        sizes_lahan = [forest_profile["production_forest_block_ha"], forest_profile["hhbk_block_ha"], forest_profile["community_block_ha"]]
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        ax2.pie(sizes_lahan, labels=["Produksi", "HHBK", "Komunitas"], autopct="%1.1f%%", startangle=140, colors=["#2E7D32", "#81C784", "#C8E6C9"])
        st.pyplot(fig2)

# --- HALAMAN 4: PRODUKSI MAKRO ---
elif selected == "Produksi Makro":
    st.title("💰 Analisis Produksi & Pendapatan Kawasan")
    st.write("---")
    
    st.metric(label="Total Estimasi Pendapatan Makro (Sektor Pasar)", value=f"Rp {total_income_miliar:.2f} Miliar/Tahun")
    st.write("### Matriks Ekonomi Nilai Komoditas")
    st.dataframe(df_makro, use_container_width=True)

# --- HALAMAN 5: RENCANA AKSI & INVESTASI ---
elif selected == "Rencana Aksi & Investasi":
    st.title("🌱 Rencana Restorasi Lahan & Kelayakan Finansial Mikro")
    st.write("---")
    
    st.subheader("Strategi Aksi Pemulihan Vegetasi")
    st.dataframe(df_restorasi, use_container_width=True)
    
    st.write("---")
    st.subheader("Analisis Proyeksi Kelayakan Investasi Mikro")
    st.dataframe(df_kelayakan, use_container_width=True)