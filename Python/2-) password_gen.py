import random

def sifre_olustur():
    print("\n--- Güçlü Şifre Oluşturucu ---")
    
    # 1. Kullanıcıdan uzunluğu al
    uzunluk = int(input("Şifre uzunluğu kaç olsun? (Örn: 8, 12): "))
    
    # 2. Kullanılacak karakter havuzunu tanımla
    kucuk_harfler = "abcdefghijklmnopqrstuvwxyz"
    buyuk_harfler = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rakamlar = "0123456789"
    semboller = "!@#$%^&*()_+"
    
    # Tüm karakterleri tek bir havuzda toplayalım
    tum_karakterler = kucuk_harfler + buyuk_harfler + rakamlar + semboller
    
    olusan_sifre = ""
    
    # 3. Rastgele karakterler seçerek şifre oluştur
    for i in range(uzunluk):
        # Havuzdan rastgele bir karakter seç
        rastgele_karakter = random.choice(tum_karakterler)
        # Seçilen karakteri şifremize ekle
        olusan_sifre += rastgele_karakter

    print(f"Oluşturulan Şifre: {olusan_sifre}")

# Programı çalıştır
while True:
    sifre_olustur()
    
    devam = input("\nYeni şifre oluşturulsun mu? (e/h): ")
    if devam == "h":
        print("Görüşmek üzere!")
        break