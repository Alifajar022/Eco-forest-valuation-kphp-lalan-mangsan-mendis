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
# 3. SIDEBAR NAVIGATION (GAYA KPH CEPU)
# ==========================================
with st.sidebar:
    # Menampilkan Logo Unisba paling atas di sidebar
    st.image("logo unisba.jpg", use_container_width=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Eco-Forest Valuation</h3>", unsafe_allow_html=True)
    
    # Menu Navigasi Vertikal Bulat-Bulat
    selected = option_menu(
        menu_title="Navigasi",
        options=["Beranda", "Profil Hutan", "Produksi Makro", "Rencana Aksi & Investasi"],
        icons=["house", "tree", "currency-dollar", "graph-up-arrow"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px!", "background-color": "transparent"},
            "icon": {"color": "#E53935", "font-size": "16px"}, # Warna merah bulat ikon acuan
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#333333"},
            "nav-link-selected": {"background-color": "#212121"},
        }
    )
    
    st.write("---")
    st.header("⚙️ Parameter Simulasi")
    price_wood = st.slider("Harga Kayu (Rp/m³)", 1000000, 2500000, 1618000, step=50000)
    price_jelutung = st.slider("Harga Jelutung (Rp/kg)", 50000, 150000, 90000, step=5000)
    price_karet = st.slider("Harga Karet (Rp/kg)", 10000, 40000, 20000, step=1000)


# ==========================================
# 4. OPERASI HITUNG DATA
# ==========================================
wood_income = wood_production["annual_volume_m3"] * price_wood
jelutung_income = hhbk_production["jelutung_kg"] * price_jelutung
karet_income = hhbk_production["karet_kg"] * price_karet
total_income_miliar = (wood_income + jelutung_income + karet_income) / 1_000_000_000

df_makro = pd.DataFrame({
    "Komoditas": ["Kayu", "Jelutung", "Karet"],
    "Volume Produksi": [wood_production["annual_volume_m3"], hhbk_production["jelutung_kg"], hhbk_production["karet_kg"]],
    "Satuan": ["m³", "Kg", "Kg"],
    "Harga Simulasi": [price_wood, price_jelutung, price_karet],
    "Total Pendapatan": [wood_income, jelutung_income, karet_income]
})


# ==========================================
# 5. KONDISIONAL HALAMAN (KONTEN UTAMA)
# ==========================================

# --- HALAMAN 1: BERANDA ---
if selected == "Beranda":
    st.title("🌳 Eco-Forest Valuation KPHP Lalan Mangsang Mendis")
    st.write("PBL 6 — Ekonomi Sumber Daya Hutan")
    st.write("---")
    
    st.header("Mata Kuliah")
    st.write("Ekonomi Sumber Daya Alam dan Lingkungan")
    
    st.header("Dosen Pengampu")
    st.write("Yuhka Sundaya, S.E., M.Si.")
    
    # Kotak Kelompok Hijau Gelap Identitas Anda
    st.markdown("""
    <div style="background-color: #112E14; padding: 15px; border-radius: 8px; color: #81C784;">
        <b style="color: #FFFFFF;">KELOMPOK 4</b><br>
        • Ali Fajar Maulana (10090222056)
    </div>
    """, unsafe_allow_html=True)

# --- HALAMAN 2: PROFIL HUTAN ---
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

# --- HALAMAN 3: PRODUKSI MAKRO ---
elif selected == "Produksi Makro":
    st.title("💰 Analisis Produksi & Pendapatan Kawasan")
    st.write("---")
    
    st.metric(label="Total Estimasi Pendapatan Makro", value=f"Rp {total_income_miliar:.2f} Miliar/Tahun")
    st.write("### Matriks Ekonomi Nilai Komoditas")
    st.dataframe(df_makro, use_container_width=True)

# --- HALAMAN 4: RENCANA AKSI & INVESTASI ---
elif selected == "Rencana Aksi & Investasi":
    st.title("🌱 Rencana Restorasi Lahan & Kelayakan Finansial Mikro")
    st.write("---")
    
    st.subheader("Strategi Aksi Pemulihan Vegetasi")
    st.dataframe(df_restorasi, use_container_width=True)
    
    st.write("---")
    st.subheader("Analisis Proyeksi Kelayakan Investasi Mikro")
    st.dataframe(df_kelayakan, use_container_width=True)