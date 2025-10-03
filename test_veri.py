import os
import json

# Dosya yolunu tanımla - veri klasörünün içindeki bitki_bilgi.json dosyası
dosya_yolu = "veri/bitki_bilgi.json"

# Dosya yolunun tam konumunu ekrana yazdır
# os.path.abspath fonksiyonu, dosyanın sistemdeki tam yolunu verir
print("Kontrol edilen dosya yolu:", os.path.abspath(dosya_yolu))

# Dosyanın varlığını kontrol et
if not os.path.exists(dosya_yolu):
    print("❌ Dosya bulunamadı!")  # Dosya yoksa hata mesajı göster
else:
    try:
        # JSON dosyasını aç ve içeriğini oku
        # encoding="utf-8" parametersi Türkçe karakterlerin düzgün okunmasını sağlar
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            bitki_veri = json.load(f)
        
        # Dosya başarıyla okundu mesajı
        print("\n✅ Dosya başarıyla yüklendi!")
        
        # Sorunları ve nedenlerini listele
        print("\n--- Sorunlar ---")
        for sorun, nedenler in bitki_veri["sorunlar"].items():
            # Her satırda bir sorun ve onun olası nedenleri gösterilir
            print(f"{sorun} → {', '.join(nedenler)}")
        
        # Bakım önerilerini listele
        print("\n--- Bakım Önerileri ---")
        for sorun, oneriler in bitki_veri["bakim_onerileri"].items():
            # Her satırda bir sorun nedeni ve onun için önerilen çözümler gösterilir
            print(f"{sorun} → {oneriler}")
    
    # Hata yönetimi blokları
    except json.JSONDecodeError as e:
        # JSON formatı hatalıysa özel hata mesajı göster
        print("\n❌ JSON biçim hatası:", e)
    except Exception as e:
        # Diğer tüm hatalar için genel hata mesajı göster
        print("\n❌ Dosya okunamadı:", e)