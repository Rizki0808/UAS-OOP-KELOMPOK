from flask import Flask, render_template
import requests
from googletrans import Translator

app = Flask(__name__)

API_URL = "https://fakestoreapi.com/products"

# Buat objek penerjemah
translator = Translator()

# Fungsi konversi USD ke Rupiah
def to_rupiah(usd):
    rate = 15000  # kurs konversi
    return f"Rp {usd * rate:,.0f}".replace(",", ".")

@app.route('/')
def index():
    response = requests.get(API_URL)
    products = response.json()

    # Ubah harga ke Rupiah
    for p in products:
        p['price_rp'] = to_rupiah(p['price'])

    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    response = requests.get(f"{API_URL}/{product_id}")
    product = response.json()

    # Tambahkan harga dalam Rupiah
    product['price_rp'] = to_rupiah(product['price'])

    # Coba terjemahkan deskripsi ke Bahasa Indonesia
    try:
        translated = translator.translate(product['description'], src='en', dest='id')
        product['description_id'] = translated.text
    except Exception as e:
        print("❌ Terjadi error saat menerjemahkan:", e)
        product['description_id'] = product['description']  # tampilkan teks asli kalau gagal

    return render_template('detail.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)