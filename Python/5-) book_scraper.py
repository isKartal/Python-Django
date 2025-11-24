import requests
from bs4 import BeautifulSoup

def kitaplari_getir():
    # 1. Hedef siteye istek at
    url = "http://books.toscrape.com/"
    print(f"📡 {url} adresine bağlanılıyor...")
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Hata: Siteye erişilemedi!")
        return

    # 2. Gelen HTML içeriğini 'BeautifulSoup' ile parçalanabilir hale getir
    # Buna "Çorba (Soup) yapmak" denir :)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 3. Kitapları bul
    # Sitede her kitap <article class="product_pod"> etiketi içindedir.
    kitaplar = soup.find_all("article", class_="product_pod")
    
    print(f"✅ Toplam {len(kitaplar)} kitap bulundu.\n")
    print(f"{'KİTAP ADI':<50} | {'FİYAT'}")
    print("-" * 65)

    # 4. Her bir kitabın içindeki detayları çek
    for kitap in kitaplar:
        # Kitap adı <h3> etiketinin içindeki <a> etiketinin 'title' özelliğinde gizli
        baslik_elementi = kitap.find("h3").find("a")
        kitap_adi = baslik_elementi["title"]
        
        # Fiyat <p class="price_color"> içinde
        fiyat_elementi = kitap.find("p", class_="price_color")
        fiyat = fiyat_elementi.text
        
        # Listeye yazdır (<50 diyerek hizalama yapıyoruz)
        print(f"{kitap_adi:<50} | {fiyat}")

if __name__ == "__main__":
    kitaplari_getir()