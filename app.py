import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="KPHP Lalan Mangsang Mendis", layout="wide")

st.markdown("""
<style>
.kpi{
padding:15px;border-radius:12px;background:#e8f5e9;
border-left:6px solid #2e7d32;margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

forest_area = 259940
production_block = 166164.92
hhbk_block = 34675.90
community_block = 59099.18

wood = 440000
jelutung = 697796
karet = 3241005
nipah = 325000
nanas = 42000
ikan = 58150

st.title("🌳 ECO-FOREST KPHP LALAN MANGSANG MENDIS")

try:
    st.image("logo unisba.jpg", width=180)
    st.subheader("Dashboard Produksi, Pendapatan, dan Restorasi")
    st.markdown("""
<div style="
padding:15px;
border-radius:10px;
background-color:#f1f8e9;
border-left:6px solid #2e7d32;
margin-bottom:20px;
">

<b>Dosen Pengampu</b> :
                
Yuhka Sundaya, S.E., M.Si.<br><br>
                
<h3>👨‍🎓 Identitas Penyusun</h3>
<b>Nama Mahasiswa</b> :<br>
• Azrial Rafsanzanni (10090222067)<br>
• Ali Fajar Maulana (10090222056)<br><br>

<b>Mata Kuliah</b> : Ekonomi Sumber Daya Alam & Lingkungan<br>
<b>Program Studi</b> : Ekonomi Pembangunan<br>
<b>Universitas</b> : Universitas Islam Bandung (UNISBA)

</div>
""", unsafe_allow_html=True)
except:
    pass

st.sidebar.header("Simulasi Harga")
p_kayu = st.sidebar.slider("Kayu",1000000,2500000,1618000,50000)
p_jel = st.sidebar.slider("Jelutung",50000,150000,90000,5000)
p_kar = st.sidebar.slider("Karet",10000,40000,20000,1000)
p_nip = st.sidebar.slider("Nipah",2000,10000,5000,500)
p_nan = st.sidebar.slider("Nanas",1000,8000,3000,500)
p_ika = st.sidebar.slider("Ikan",15000,60000,30000,1000)

income = {
    "Kayu": wood*p_kayu,
    "Jelutung": jelutung*p_jel,
    "Karet": karet*p_kar,
    "Nipah": nipah*p_nip,
    "Nanas": nanas*p_nan,
    "Ikan": ikan*p_ika
}

total = sum(income.values())

tab1,tab2,tab3,tab4 = st.tabs(["Ringkasan","Data","Visualisasi","Restorasi"])

with tab1:
    c1,c2,c3 = st.columns(3)
    c1.metric("Luas Kawasan", f"{forest_area:,.0f} Ha")
    c2.metric("Produksi Kayu", f"{wood:,.0f} m3")
    c3.metric("Pendapatan", f"Rp {total/1e9:.2f} Miliar")

with tab2:
    df = pd.DataFrame({
        "Komoditas": list(income.keys()),
        "Pendapatan (Rp)": list(income.values())
    })
    st.dataframe(df, use_container_width=True)
    st.download_button("Download CSV", df.to_csv(index=False), "kphp.csv")

with tab3:
    col1,col2 = st.columns(2)

    with col1:
        fig,ax=plt.subplots()
        ax.bar(df["Komoditas"], df["Pendapatan (Rp)"]/1e9)
        ax.set_ylabel("Miliar Rp")
        ax.set_title("Pendapatan Komoditas")
        st.pyplot(fig)

    with col2:
        fig2,ax2=plt.subplots()
        ax2.pie(
            [production_block,hhbk_block,community_block],
            labels=["Produksi","HHBK","Pemberdayaan"],
            autopct="%1.1f%%"
        )
        ax2.set_title("Distribusi Lahan")
        st.pyplot(fig2)

with tab4:
    restorasi = pd.DataFrame({
        "Lokus":["HP Lalan","Muara Medak","HP Mangsang","Gambut"],
        "Luas":[1000,1000,500,500]
    })
    st.dataframe(restorasi, use_container_width=True)

    fig3,ax3=plt.subplots()
    ax3.pie(restorasi["Luas"], labels=restorasi["Lokus"], autopct="%1.1f%%")
    st.pyplot(fig3)

    kelayakan = pd.DataFrame({
        "Komoditas":["Jelutung","Kenaf","Sengon","Nilam","Nursery"],
        "NPV":[41664172746,4557258660,3165145633,2672971229,376725634],
        "BCR":[1.71,1.41,1.21,1.16,1.55]
    })

    st.dataframe(kelayakan, use_container_width=True)

    fig4,ax4=plt.subplots()
    ax4.barh(kelayakan["Komoditas"], kelayakan["NPV"]/1e9)
    ax4.set_xlabel("NPV (Miliar Rp)")
    st.pyplot(fig4)
