import json

VERI_DOSYASI = "veri/bitki_bilgi.json"

def veri_yukle():
    """
    JSON dosyasını okur ve veri olarak döndürür.
    Dosya okunamazsa boş bir sözlük döner.
    """
    try:
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"sorunlar": {}, "bakim_onerileri": {}}

def sorun_tespit(kullanici_girdisi: str):
    """
    Kullanıcıdan gelen cümlenin içindeki anahtar kelimeler ve anlam yakınlığına 
    bakarak en uygun sorunu bulur ve ilgili nedenleri döner.
    Eşleşme yöntemleri:
      - Tam eşleşme.
      - Cümlenin anahtar kelime parçalarının çoğunu içerme (fuzzy-matching benzeri).
      - Synonym/benzerlik ("sararma", "yaprak sararıyor", "sararmış yaprak", v.b.).

    Giriş yoksa veya hiçbir şey eşleşmezse "Sorun bulunamadı" döner.
    """
    if not kullanici_girdisi:
        return ["Sorun bulunamadı"]
    veri = veri_yukle()
    sorunlar = veri.get("sorunlar", {})
    kullanici_girdisi = kullanici_girdisi.lower()

    # 1. Tam eşleşme
    if kullanici_girdisi in sorunlar:
        return sorunlar[kullanici_girdisi]

    # 2. Anahtar cümle parçalarıyla akıllı (kelime bazlı) eşleşme
    eslesmeler = []
    for anahtar, nedenler in sorunlar.items():
        anahtar_kelimeler = anahtar.split()
        # Kaç kelime cümlede geçiyor
        ortak_sayi = sum(1 for kelime in anahtar_kelimeler if kelime in kullanici_girdisi)
        if ortak_sayi == len(anahtar_kelimeler):      # Tüm kelimeler eşleştiyse (tam yakın)
            return nedenler
        elif ortak_sayi >= max(1, int(len(anahtar_kelimeler) / 2)):  # %50'den fazlası eşleştiyse
            eslesmeler.append((ortak_sayi, nedenler))
    if eslesmeler:
        # En çok ortak kelimeli eşleşmeyi döndür
        return sorted(eslesmeler, key=lambda x: x[0], reverse=True)[0][1]

    # 3. Anahtarın herhangi birinin cümlede bulunması
    for anahtar, nedenler in sorunlar.items():
        if anahtar in kullanici_girdisi or kullanici_girdisi in anahtar:
            return nedenler

    # 4. Hiçbiri değilse
    return ["Sorun bulunamadı"]

def cozum_oner(sorun: str):
    veri = veri_yukle()
    bakim_onerileri = veri.get("bakim_onerileri", {})
    sorun_norm = sorun.strip().lower().replace("ı","i").replace("ü","u").replace("ç","c").replace("ö","o").replace("ş","s").replace("ğ","g")

    # 1. Tam eşleşme
    if sorun in bakim_onerileri:
        return bakim_onerileri[sorun]

    # 2. Normalize anahtarlarla eşleşme
    for anahtar in bakim_onerileri:
        anahtar_norm = anahtar.strip().lower().replace("ı","i").replace("ü","u").replace("ç","c").replace("ö","o").replace("ş","s").replace("ğ","g")
        if anahtar_norm == sorun_norm:
            return bakim_onerileri[anahtar]
        # Ekstra: Eğer anahtar, sorun içinde veya sorun, anahtar içinde geçiyorsa (parça eşleşme)
        if sorun_norm in anahtar_norm or anahtar_norm in sorun_norm:
            return bakim_onerileri[anahtar]

    # 3. Kelime tabanlı en çok ortak içeren anahtar (bonus hassasiyet)
    sorun_kelimeler = set(sorun_norm.split())
    max_ortak = 0
    en_iyi_oneri = None
    for anahtar in bakim_onerileri:
        anahtar_norm = anahtar.strip().lower().replace("ı","i").replace("ü","u").replace("ç","c").replace("ö","o").replace("ş","s").replace("ğ","g")
        anahtar_kelimeler = set(anahtar_norm.split())
        ortak = len(anahtar_kelimeler & sorun_kelimeler)
        if ortak > max_ortak:
            max_ortak = ortak
            en_iyi_oneri = bakim_onerileri[anahtar]
    if max_ortak > 0:
        return en_iyi_oneri

    return ["Bu sorun için öneri bulunamadı"]