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
# 3. SIDEBAR NAVIGATION (6 SUB-BAB)
# ==========================================
with st.sidebar:
    st.image("logo unisba.jpg", use_container_width=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Eco-Forest Valuation</h3>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="Navigasi",
        options=["Beranda", "Profil Hutan", "Analisis Tegakan", "Valuasi TEV", "Analisis Trade-Off", "Rencana Aksi & Investasi"],
        icons=["house", "tree", "bar-chart-steps", "calculator", "arrow-left-right", "graph-up-arrow"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px!", "background-color": "transparent"},
            "icon": {"color": "#E53935", "font-size": "16px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#333333"},
            "nav-link-selected": {"background-color": "#212121"},
        }
    )


# ==========================================
# 4. KONDISIONAL HALAMAN (KONTEN UTAMA)
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
    Melalui instrumen dashboard ini, kami mensimulasikan nilai ekonomi dari komoditas unggulan 
    sekaligus memetakan rencana aksi restorasi vegetasi serta uji kelayakan finansial proyek secara terintegrasi.
    """)

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

# --- HALAMAN 3: ANALISIS TEGAKAN ---
elif selected == "Analisis Tegakan":
    st.title("📊 Analisis Potensi Tegakan & Hasil Hutan Makro")
    st.write("---")
    
    # Masukkan slider khusus parameter ekonomi di sini
    st.subheader("⚙️ Parameter Harga Pasar")
    price_wood = st.slider("Harga Kayu (Rp/m³)", 1000000, 2500000, 1618000, step=50000)
    price_jelutung = st.slider("Harga Jelutung (Rp/kg)", 50000, 150000, 90000, step=5000)
    price_karet = st.slider("Harga Karet (Rp/kg)", 10000, 40000, 20000, step=1000)
    
    wood_income = wood_production["annual_volume_m3"] * price_wood
    jelutung_income = hhbk_production["jelutung_kg"] * price_jelutung
    karet_income = hhbk_production["karet_kg"] * price_karet
    total_income_miliar = (wood_income + jelutung_income + karet_income) / 1_000_000_000

    df_makro = pd.DataFrame({
        "Komoditas": ["Kayu", "Jelutung", "Karet"],
        "Volume Produksi/Tahun": [wood_production["annual_volume_m3"], hhbk_production["jelutung_kg"], hhbk_production["karet_kg"]],
        "Satuan": ["m³", "Kg", "Kg"],
        "Harga Simulasi (Rp)": [price_wood, price_jelutung, price_karet],
        "Total Pendapatan (Rp)": [wood_income, jelutung_income, karet_income]
    })
    
    st.write("---")
    st.metric(label="Total Estimasi Pendapatan Sektor Ekonomi Pasar", value=f"Rp {total_income_miliar:.2f} Miliar/Tahun")
    st.dataframe(df_makro, use_container_width=True)
    
    st.markdown("""
    > **Interpretasi Data Tegakan:**
    > Sektor pemanfaatan hasil hutan (tangible benefits) KPHP Lalan didominasi kuat oleh komoditas kayu produksi struktural, disusul oleh komoditas Hasil Hutan Bukan Kayu (HHBK) berbasis pemberdayaan masyarakat seperti komoditas karet rawa dan getah jelutung makro. Fluktuasi harga pasar komoditas ini berpengaruh langsung pada sumbangan Pendapatan Asli Daerah (PAD).
    """)

# --- HALAMAN 4: VALUASI TEV ---
elif selected == "Valuasi TEV":
    st.title("🧮 Valuasi Nilai Ekonomi Total (Total Economic Value - TEV)")
    st.write("---")
    
    # Parameter Khusus TEV
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.subheader("⚙️ Parameter Ekologi Base")
        carbon_value_ha = st.slider("Nilai Serapan Karbon (Rp/Ha/Tahun)", 500000, 5000000, 2000000, step=100000)
        water_service_ha = st.slider("Nilai Fungsi Tata Air (Rp/Ha/Tahun)", 100000, 2000000, 1000000, step=50000)
    with col_p2:
        st.subheader("⚙️ Simulasi Kerusakan Ekosistem")
        kerusakan = st.slider("Tingkat Kerusakan Hutan (Luas/Ha)", min_value=0, max_value=100, value=10, step=5, format="%d%%")
        
    # Hitung Komponen TEV
    nilai_ekonomi_tetap = 711.9 + 62.8 + 64.8 # Nilai Ekonomi Pasar Konstan (Miliar)
    nilai_ekologi_base = ((forest_profile["forest_area_ha"] * carbon_value_ha) + (forest_profile["forest_area_ha"] * water_service_ha)) / 1_000_000_000
    
    tev_awal = nilai_ekonomi_tetap + nilai_ekologi_base
    kehilangan_jasa_lingkungan = nilai_ekologi_base * (kerusakan / 100)
    tev_setelah_degradasi = tev_awal - kehilangan_jasa_lingkungan
    persen_penurunan = ((tev_setelah_degradasi - tev_awal) / tev_awal) * 100

    # Tampilan Metrik Seperti di Foto
    st.write("---")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="Kerusakan", value=f"{kerusakan}%")
    with col_m2:
        st.metric(label="TEV Awal (Kondisi Ideal)", value=f"Rp {tev_awal:.1f} Miliar")
    with col_m3:
        st.metric(label="TEV Setelah Degradasi", value=f"Rp {tev_setelah_degradasi:.1f} Miliar", delta=f"{persen_penurunan:.1f}%")
        
    if kerusakan <= 15:
        st.success("Kondisi hutan masih relatif baik dan stabil.")
    elif kerusakan <= 40:
        st.warning("Status Waspada! Degradasi mulai menggerus nilai manfaat fungsi tata air gambut.")
    else:
        st.error("Status Kritis! Ekosistem rawa gambut mengalami degradasi parah, membutuhkan tindakan darurat.")

    # PENJELASAN AKADEMIK DI BAWAH SIMULASI
    st.write("---")
    st.subheader("🔍 Penjelasan Teoretis Valuasi Ekonomi")
    st.markdown(f"""
    Pendekatan **Total Economic Value (TEV)** membagi nilai kegunaan hutan menjadi dua kelompok besar:
    1. **Nilai Guna Langsung (Direct Use Value):** Diperoleh dari pemanfaatan fisik barang pasar seperti kayu dan HHBK (Tercatat konstan menyumbang **Rp {nilai_ekonomi_tetap:.1f} Miliar**).
    2. **Nilai Guna Tidak Langsung (Indirect Use Value):** Berupa fungsi ekologi penyerapan karbon dan pengatur hidrologi lahan basah (Nilai simulasi saat ini: **Rp {nilai_ekologi_base - kehilangan_jasa_lingkungan:.1f} Miliar** dari potensi maksimal **Rp {nilai_ekologi_base:.1f} Miliar**).
    
    **Analisis Dampak Simulasi:**
    Ketika tingkat kerusakan berada pada angka **{kerusakan}%**, ekosistem kehilangan kemampuan jasa lingkungannya sebesar **Rp {kehilangan_jasa_lingkungan:.1f} Miliar**. Kerugian ekologis ini sering kali tidak tercatat dalam akuntansi ekonomi konvensional karena bersifat *non-market commodity*, padahal dampaknya nyata memicu penurunan daya dukung lingkungan wilayah Sumatera Selatan.
    """)

# --- HALAMAN 5: ANALISIS TRADE-OFF ---
elif selected == "Analisis Trade-Off":
    st.title("🔄 Analisis Konflik Kepentingan & Efek Trade-Off")
    st.write("---")
    
    st.subheader("⚙️ Parameter Kebijakan Pemanfaatan Kawasan")
    st.markdown("Geser intensitas eksploitasi untuk melihat bagaimana keuntungan ekonomi mengorbankan jasa lingkungan:")
    intensitas_tebang = st.slider("Intensitas Eksploitasi Kayu Komersial (%)", 0, 100, 60, step=10)
    
    # Model Matematika Konseptual Trade-off
    manfaat_ekonomi = 711.9 * (intensitas_tebang / 100) + 127.6 # Kayu linear naik + HHBK stabil
    manfaat_ekologi = 779.8 * (1.0 - (intensitas_tebang / 100) ** 2) # Penurunan ekologi non-linear (makin botak makin hancur ekologinya)
    tev_gabungan = manfaat_ekonomi + manfaat_ekologi
    
    # Visualisasi Grafik Batang Komparatif
    df_trade = pd.DataFrame({
        "Komponen Sektor": ["Manfaat Pasar (Ekonomi)", "Manfaat Non-Pasar (Ekologi)", "Total Nilai Ekonomi Kawasan (TEV)"],
        "Nilas Valuasi (Miliar Rp)": [manfaat_ekonomi, manfaat_ekologi, tev_gabungan]
    })
    
    fig_trade = px.bar(
        df_trade, x="Komponen Sektor", y="Nilas Valuasi (Miliar Rp)", color="Komponen Sektor",
        color_discrete_sequence=["#E53935", "#2E7D32", "#1565C0"], text_auto='.1f',
        title=f"Keseimbangan Nilai Kawasan pada Intensitas Eksploitasi {intensitas_tebang}%"
    )
    st.plotly_chart(fig_trade, use_container_width=True)
    
    # PENJELASAN MENDALAM TENTANG TARIK MENARIK (TRADE-OFF)
    st.write("---")
    st.subheader("⚖️ Esensi Fenomena Trade-Off (Tarik-Menarik Manfaat)")
    st.markdown(f"""
    Dalam ekonomi sumber daya alam, **Trade-off** adalah situasi penarikan keputusan di mana keuntungan di satu sektor secara mutlak menuntut pengorbanan di sektor lainnya. Di kawasan KPHP Lalan, dinamika tarik-menarik ini terjadi secara tajam antara **Peningkatan Pendapatan Finansial Daerah** dan **Keberlanjutan Fungsi Jasa Ekosistem Gambut**.
    
    *   **Ketika Eksploitasi Rendah (0% - 30%):** Keuntungan ekonomi dari produksi kayu sangat minim, namun nilai pelestarian lingkungan berada pada tingkat klimaks. Kawasan berfungsi penuh sebagai penahan emisi karbon.
    *   **Ketika Eksploitasi Maksimal ({intensitas_tebang}% - 100%):** Pendapatan dari sektor perkayuan melonjak naik hingga mencapai angka tertinggi. Namun, konsekuensi *trade-off* ekologis yang harus dibayar adalah hancurnya nilai ekologi secara eksponensial (menurun drastis menjadi sisa **Rp {manfaat_ekologi:.1f} Miliar**). 
    
    **Rekomendasi Kebijakan (Optimum Management):**
    Grafik di atas membuktikan bahwa pemanfaatan hutan tidak boleh dilakukan secara eksploitatif (100%). Poin keseimbangan terbaik dicapai melalui pengelolaan multi-pihak, yaitu membatasi tebangan kayu tahunan dan beralih mengoptimalkan komoditas non-kayu (Karet & Jelutung) yang tidak merusak tegakan utama rawa gambut.
    """)

# --- HALAMAN 6: RENCANA AKSI & INVESTASI ---
elif selected == "Rencana Aksi & Investasi":
    st.title("🌱 Rencana Restorasi Lahan & Kelayakan Finansial Mikro")
    st.write("---")
    
    st.subheader("Strategi Aksi Pemulihan Vegetasi")
    st.dataframe(df_restorasi, use_container_width=True)
    
    st.write("---")
    st.subheader("Analisis Proyeksi Kelayakan Investasi Mikro")
    st.dataframe(df_kelayakan, use_container_width=True)