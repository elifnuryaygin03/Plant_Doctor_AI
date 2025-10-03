# ana_basit.py (test için)
import streamlit as st
import araclar

# Sayfa yapılandırması
st.set_page_config(page_title="Bitki Doktoru", page_icon="🌿")

st.title("🌱 Bitki Doktoru")

# Kullanıcı girdisi
kullanici_girdisi = st.text_area("Bitkinizdeki sorunu anlatın:", height=150)

if st.button("Analiz Et"):
    if kullanici_girdisi:
        with st.spinner("Analiz yapılıyor..."):
            nedenler = araclar.sorun_tespit(kullanici_girdisi)
            
            if "Sorun bulunamadı" not in nedenler:
                st.success("Analiz tamamlandı!")
                
                for neden in nedenler:
                    st.write(f"**Neden:** {neden}")
                    oneriler = araclar.cozum_oner(neden)
                    st.info(f"**Öneri:** {', '.join(oneriler)}")
            else:
                st.warning("Bu açıklamada bilinen bir sorun tespit edilemedi.")
    else:
        st.warning("Lütfen bitkinizdeki sorunu anlatın.")