import os       # Klasör oluşturma, dosya listeleme işleri için
import shutil   # Dosya taşıma (move) işleri için

def dosyalari_duzenle():
    # 1. Hangi klasörü düzenleyeceğiz?
    hedef_klasor = "daginik_klasor"
    
    # Klasör var mı diye kontrol edelim (Güvenlik)
    if not os.path.exists(hedef_klasor):
        print(f"Hata: '{hedef_klasor}' bulunamadı! Önce setup_test.py'yi çalıştır.")
        return

    # 2. Kurallarımızı Tanımlayalım (Hangi uzantı nereye gidecek?)
    # Sözlük yapısı (Dictionary) kullanıyoruz.
    klasor_kurallari = {
        "Resimler": [".jpg", ".jpeg", ".png", ".gif"],
        "Belgeler": [".pdf", ".txt", ".docx", ".xlsx"],
        "Videolar": [".mp4", ".mov", ".avi"],
        "Programlar": [".exe", ".msi", ".sh"]
    }

    print(f"📂 '{hedef_klasor}' taranıyor...\n")

    # 3. Klasördeki tüm dosyaları tek tek gez
    for dosya_adi in os.listdir(hedef_klasor):
        
        # Dosyanın tam yolunu oluştur (daginik_klasor/resim.jpg)
        dosya_yolu = os.path.join(hedef_klasor, dosya_adi)

        # Eğer bu bir klasörse atla (sadece dosyaları taşıyacağız)
        if os.path.isdir(dosya_yolu):
            continue

        # Dosyanın uzantısını al (os.path.splitext ismi ve uzantıyı ayırır)
        # Örn: 'tatil.jpg' -> ('tatil', '.jpg')
        dosya_uzantisi = os.path.splitext(dosya_adi)[1].lower() # küçük harfe çevir

        # 4. Dosyanın nereye gideceğine karar ver
        tasindi_mi = False
        
        for klasor_adi, uzantilar in klasor_kurallari.items():
            if dosya_uzantisi in uzantilar:
                
                # Hedef alt klasör yolunu oluştur (daginik_klasor/Resimler)
                hedef_alt_klasor = os.path.join(hedef_klasor, klasor_adi)
                
                # Eğer o klasör yoksa oluştur!
                os.makedirs(hedef_alt_klasor, exist_ok=True)
                
                # Dosyayı taşı
                yeni_yol = os.path.join(hedef_alt_klasor, dosya_adi)
                shutil.move(dosya_yolu, yeni_yol)
                
                print(f"✅ {dosya_adi} -> {klasor_adi} içine taşındı.")
                tasindi_mi = True
                break # Doğru klasörü bulduk, diğerlerine bakmaya gerek yok
        
        # Eğer hiçbir kategoriye uymuyorsa "Diğer" klasörüne atalım
        if not tasindi_mi:
            diger_klasor = os.path.join(hedef_klasor, "Diger")
            os.makedirs(diger_klasor, exist_ok=True)
            shutil.move(dosya_yolu, os.path.join(diger_klasor, dosya_adi))
            print(f"⚪ {dosya_adi} -> Diger içine taşındı.")

    print("\n✨ Düzenleme tamamlandı!")

if __name__ == "__main__":
    dosyalari_duzenle()