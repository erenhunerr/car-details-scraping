import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.arabam.com"


base_page_url = "https://www.arabam.com/ikinci-el/otomobil?page="
page_numbers = range(252, 253)
urls = [base_page_url + str(page) for page in page_numbers]


products = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    product_list = soup.find_all('tr', class_='listing-list-item should-hover bg-white')
    
    for product in product_list:
        product_detail_path = product.find('a', class_='link-overlay').get('href')

        product_detail_url = base_url + product_detail_path
        
        product_response = requests.get(product_detail_url)
        product_soup = BeautifulSoup(product_response.text, 'html.parser')
        
        product_info = {'Ürün Adı': '', 'Fiyatı': '', 'Diğer Bilgiler': {}}
        product_name_container = product_soup.find('div', class_='product-name-container')
        if product_name_container:
            product_info['Ürün Adı'] = product_name_container.text.strip()
        
        product_price_container = product_soup.find('div', class_='product-price')
        if product_price_container:
            product_info['Fiyatı'] = product_price_container.text.strip()

        property_values = product_soup.find_all('div', class_='property-item')
        for pv in property_values:
            prop_name = pv.find('div', class_='property-key').text.strip()
            prop_value = pv.find('div', class_='property-value').text.strip()
            product_info['Diğer Bilgiler'][prop_name] = prop_value
        
        products.append(product_info)

csv_file = "arabam_urunler.csv"

with open(csv_file, mode='a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    headers = ['Ürün Adı', 'Fiyatı']
    for product in products:
        for key in product['Diğer Bilgiler'].keys():
            if key not in headers:
                headers.append(key)
    writer.writerow(headers)

    for product in products:
        row = [product['Ürün Adı'], product['Fiyatı']]
        for key in headers[2:]:
            if key in product['Diğer Bilgiler']:
                row.append(product['Diğer Bilgiler'][key])
            else:
                row.append("")
        writer.writerow(row)

print("Veriler CSV dosyasına başarıyla yazıldı:", csv_file)
