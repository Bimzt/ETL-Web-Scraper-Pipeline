import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def scrape_data():
    all_data = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        with requests.Session() as session:
            session.headers.update(headers)
            
            for page in range(1, 51):
                if page == 1:
                    url = "https://fashion-studio.dicoding.dev/"
                else:
                    url = f"https://fashion-studio.dicoding.dev/page{page}/"
                
                try:
                    response = session.get(url, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    products = soup.find_all('div', class_='product-details')
                    
                    if not products and page == 1:
                        logging.warning("Elemen produk tidak ditemukan di Halaman 1. Website mungkin memblokir bot.")
                        break

                    for item in products:
                        title_elem = item.find('h3', class_='product-title')
                        
                        price_elem = item.find('span', class_='price')
                        if not price_elem:
                            price_elem = item.find('p', class_='price')
                        desc_elems = item.find_all('p')
                        rating = gender = color = size = None
                        for p in desc_elems:
                            text = p.get_text(strip=True)
                            if "/ 5" in text or "Rating" in text: rating = text
                            elif "Gender" in text: gender = text
                            elif "Color" in text: color = text
                            elif "Size" in text: size = text
                            elif "Invalid" in text: rating = text 
                        if len(desc_elems) >= 4 and not gender:
                            rating = desc_elems[0].get_text(strip=True)
                            gender = desc_elems[1].get_text(strip=True)
                            color = desc_elems[2].get_text(strip=True)
                            size = desc_elems[3].get_text(strip=True)

                        all_data.append({
                            "Title": title_elem.text.strip() if title_elem else None,
                            "Price": price_elem.text.strip() if price_elem else None,
                            "Rating": rating,
                            "Colors": color,
                            "Size": size,
                            "Gender": gender,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                    logging.info(f"Berhasil extract {url} | Total data sementara: {len(all_data)}")
                    
                except requests.exceptions.RequestException as e:
                    logging.error(f"Error saat mengambil data di url {url}: {e}")
                    continue
                    
    except Exception as e:
        logging.error(f"Fatal error pada tahapan ekstraksi: {e}")
        
    return all_data