import streamlit as st
from llm_yonlendirici import query_llm
import araclar

# -- ARKA PLAN GÖRSELİ --
st.markdown("""
<style>
body, .stApp {
    background-image: url("https://images.unsplash.com/photo-1465101178521-c1a9136a3c5e?auto=format&fit=crop&w=1500&q=80");
    background-size: cover;
    background-attachment: fixed;
}
.block-container {background: rgba(255,255,255,0.93);}
</style>
""", unsafe_allow_html=True)

st.title("Plant Doctor AI 🌱")

# Girdi & Fotoğraf & Açıklama
st.subheader("📸 Bitki Fotoğrafı Yükle")
bitki_foto = st.file_uploader("Fotoğraf seçin (isteğe bağlı):", type=["jpg", "jpeg", "png"])
aciklama = st.text_area("Fotoğraf için açıklama (isteğe bağlı):", "")

if bitki_foto:
    st.image(bitki_foto, caption="Yüklenen Bitki Fotoğrafı", use_container_width=True)
if aciklama:
    st.info(f"**Açıklama:** {aciklama}")

user_input = st.text_input("Bitkinizdeki sorunu yazın:")

if st.button("Analiz Et"):
    # YEREL ANALİZ
    tespit_nedenler = araclar.sorun_tespit(user_input)
    st.subheader("Yerel Veriyle Tespit Edilen Olası Nedenler:")
    st.write(tespit_nedenler)
    st.subheader("Yerel Çözüm Önerilerin:")
    for neden in tespit_nedenler:
        for oner in araclar.cozum_oner(neden):
            st.info(f"• {oner}")

    # LLM Function Call (API)
    st.subheader("Detaylı Bakım ve Çözüm (LLM Function Call ile):")
    llm_response = query_llm(user_input)
    st.markdown(f"**🌿 Tespit Edilen Sorun:** {llm_response.get('sorun', '---')}")
    st.markdown("**❗ Nedenler:**")
    for n in llm_response.get('nedenler', []):
        st.warning("· " + n)
    st.markdown("**💡 Çözüm Önerileri:**")
    for c in llm_response.get('cozum_onerileri', []):
        st.success("· " + c)
    st.markdown("**📝 Bakım Önerileri:**")
    for b in llm_response.get('bakim_onerileri', []):
        st.info("· " + b)
    if "hata" in llm_response:
        st.error(llm_response)
st.markdown("""
---
<sub>
Bu uygulama hem **yerel veri tabanını** hem de **LLM API function call** analizini birlikte sunar.
</sub>
""", unsafe_allow_html=True)