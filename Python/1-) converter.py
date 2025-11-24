def menu_goster():
    """Kullanıcıya seçenekleri gösteren basit bir fonksiyon"""
    print("\n" + "=" * 20)
    print("   BİRİM ÇEVİRİCİ   ")
    print("=" * 20)
    print("1. Sıcaklık (C <-> F)")
    print("2. Mesafe (KM <-> Mil)")
    print("q. Çıkış")

def sicaklik_cevir():
    print("\n--- Sıcaklık Çevirici ---")
    print("1. Celsius -> Fahrenheit")
    print("2. Fahrenheit -> Celsius")

    alt_secim = input("Seçiminiz (1 veya 2): ")

    if alt_secim == '1':
        c = float(input("Celsius değeri girin: "))
        f =(c * 1.8 ) + 32
        print(f"Sonuç: {c}°C = {f:.2f}°F") # .2f virgülden sonra 2 basamak gösterir

    elif alt_secim == '2':
        f = float(input("Fahrenheit değeri girin: "))
        c = (f - 32) / 1.8
        print(f"Sonuç: {f}°F = {c:.2f}°C")

    else:
        print("Geçersiz alt seçim!")

def mesafe_cevir():
    print ("\n--- Mesafe Çevirici ---")
    print("1. Kilometre -> Mil")
    print("2. Mil -> Kilometre")
    alt_secim = input("Seçiminiz (1 veya 2): ")

    if alt_secim == '1':
        km = float(input("Kilometre değeri girin: "))
        mil = km * 0.621371
        print(f"Sonuç: {km} KM = {mil:.2f} Mil")
    
    elif alt_secim == '2':
        mil = float(input("Mil değeri girin: "))
        km = mil / 0.621371
        print(f"Sonuç: {mil} Mil = {km:.2f} KM")

    else:
        print("Geçersiz alt seçim!")

# Ana Program Döngüsü
while True:
    menu_goster()

    secim = input("\nİşlem seçiniz: ")

    if secim == 'q':
        print("Programdan çıkılıyor. Görüşmek üzere!")
        break # Döngüyü kırar ve programı bitirir

    elif secim == '1':
        sicaklik_cevir()
    
    elif secim == '2':
        mesafe_cevir()
    
    else:
        print("Hatalı seçim yaptınız, lütfen tekrar deneyin.")


