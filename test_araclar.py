import araclar

# Test dosyasının çalışmaya başladığını belirt
print("test_araclar.py başladı...")

# Test için örnek kullanıcı girdisi
kullanici_girdisi = "Yapraklarım sararıyor"

# 1. Önce sorunu tespit et
# Bu adımda, kullanıcının girdiği metinde geçen anahtar kelimelere göre sorunlar tespit edilir
nedenler = araclar.sorun_tespit(kullanici_girdisi)
print("Olası nedenler:", nedenler)

# 2. Her tespit edilen neden için çözüm önerileri göster
# Her bir tespit edilen neden için veritabanındaki çözüm önerilerini alıp ekrana yazdırır
for n in nedenler:
    print(f"{n} için öneri:", araclar.cozum_oner(n))