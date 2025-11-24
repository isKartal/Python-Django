import os

def test_ortami_olustur():
    # 1. 'daginik_klasor' adında bir klasör oluştur
    klasor_adi = "daginik_klasor"
    
    if not os.path.exists(klasor_adi):
        os.mkdir(klasor_adi)
        print(f"📁 '{klasor_adi}' oluşturuldu.")
    
    # 2. İçine sahte dosyalar yaratalım
    dosyalar = [
        "tatil_fotografi.jpg",
        "odev.pdf",
        "liste.txt",
        "film.mp4",
        "fatura.pdf",
        "logo.png",
        "setup.exe",
        "muzik.mp3"
    ]
    
    for dosya in dosyalar:
        # Dosya yolunu oluştur (daginik_klasor/odev.pdf gibi)
        dosya_yolu = os.path.join(klasor_adi, dosya)
        
        # Boş bir dosya yarat (touch komutu gibi)
        with open(dosya_yolu, "w") as f:
            f.write("Bu bir test dosyasidir.")
            
    print(f"✅ '{klasor_adi}' içine {len(dosyalar)} adet test dosyası oluşturuldu.")
    print("Artık düzenleyiciyi yazmaya başlayabiliriz!")

if __name__ == "__main__":
    test_ortami_olustur()