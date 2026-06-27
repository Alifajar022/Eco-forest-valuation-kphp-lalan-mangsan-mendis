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


# ==========================================
# 4. OPERASI HITUNG DATA BASE
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
        <span style="color: #FFFFFF;">
            • Ali Fajar Maulana (10090222056)<br>
            • Azrial Rafsanzanni (10090222067)
        </span>
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
    perubahan fungsi guna tanah dan kebakaran hutan. Maka dari itu, diperlukan suatu pendekatan 
    **Penilaian Ekonomi Sumber Daya Hutan (Eco-Forest Valuation)** untuk menghitung potensi nyata kawasan. 
    Melalui instrumen dashboard ini, saya mensimulasikan nilai ekonomi makro dari komoditas unggulan 
    seperti kayu, getah jelutung, dan karet, sekaligus memetakan rencana aksi restorasi vegetasi 
    serta uji kelayakan finansial proyek mikro secara terintegrasi dan berkelanjutan.
    """)

# --- HALAMAN 2: TEV & TRADE-OFF (PERSIS SEPERTI CONTOH FOTO) ---
elif selected == "TEV & Trade-off":
    st.title("Simulasi Perubahan TEV")
    st.write("---")
    
    # 1. SLIDER KERUSAKAN HUTAN (Sesuai Layout Foto)
    kerusakan = st.slider("Kerusakan Hutan (Luas/Ha)", min_value=0, max_value=100, value=10, step=5, format="%d%%")
    
    # 2. PERHITUNGAN LOGIKA DATA (Trade-off)
    # Nilai Ekosistem Tidak Langsung KPHP Lalan (Carbon + Air + Keberadaan) = Rp 480 Miliar dalam kondisi 0% rusak
    nilai_ekologi_base = 480.0 
    nilai_ekonomi_base = total_income_miliar # Dinamis mengikuti slider harga kayu/karet
    
    tev_baru = nilai_ekonomi_base + nilai_ekologi_base
    
    # Efek Kerusakan: Mengurangi nilai ekologi secara drastis
    kehilangan_ekologi = nilai_ekologi_base * (kerusakan / 100)
    tev_setelah_degradasi = tev_baru - kehilangan_ekologi
    persen_penurunan = ((tev_setelah_degradasi - tev_baru) / tev_baru) * 100

    # 3. DISPLAY METRICS (Persis Seperti Gaya di Foto)
    st.write("### Kerusakan")
    st.header(f"{kerusakan}%")
    
    st.write("### TEV Baru")
    st.header(f"Rp {tev_baru:.1f} Miliar")
    
    st.write("### TEV Setelah Degradasi")
    st.header(f"Rp {tev_setelah_degradasi:.1f} Miliar")
    
    # Badges Indikator Penurunan Merah Merona
    if persen_penurunan < 0:
        st.markdown(f"""
        <span style="background-color: #FFEBEE; color: #C62828; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 14px;">
            ↓ {persen_penurunan:.1f}%
        </span>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <span style="background-color: #E8F5E9; color: #2E7D32; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 14px;">
            0.0%
        </span>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.write("")

    # 4. KOTAK KESIMPULAN DINAMIS (Hijau/Kuning/Merah sesuai tingkat kerusakan)
    if kerusakan <= 15:
        st.success("Kondisi hutan masih relatif baik.")
    elif kerusakan <= 40:
        st.warning("Kondisi hutan dalam status waspada. Degradasi mulai mengancam fungsi tata air gambut.")
    else:
        st.error("Kondisi hutan kritis! Gangguan ekologis tinggi, diperlukan restorasi vegetasi segera.")

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
    
    st.metric(label="Total Estimasi Pendapatan Makro", value=f"Rp {total_income_miliar:.2f} Miliar/Tahun")
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