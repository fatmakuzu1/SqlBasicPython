from groq import Groq
import psycopg2

# --- 1. Veritabanına bağlan ---
baglanti = psycopg2.connect(
    dbname="northwind",
    user="fatmakuzu",
    host="localhost"
)
cursor = baglanti.cursor()

# --- 2. Şemayı otomatik çek ---
cursor.execute("""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
""")
sema_satirlari = cursor.fetchall()

# Şemayı okunabilir bir metne çevir
sema_metni = ""
mevcut_tablo = ""
for tablo, kolon, tip in sema_satirlari:
    if tablo != mevcut_tablo:
        sema_metni += f"\n{tablo}:\n"
        mevcut_tablo = tablo
    sema_metni += f"  - {kolon} ({tip})\n"

print("--- Otomatik Çekilen Şema ---")
print(sema_metni)

# --- 3. AI Client ---
client = Groq(api_key="key")

kullanici_sorusu = "En çok sipariş veren 5 müşteriyi göster"

prompt = f"""
Sen bir SQL uzmanısın. Aşağıda gerçek veritabanı şeması var:

{sema_metni}

Kullanıcının sorusunu, YUKARIDAKİ gerçek kolon isimlerini kullanarak 
PostgreSQL sorgusuna çevir. SADECE SQL kodu yaz, başka açıklama yapma, 
markdown backtick kullanma.

Soru: {kullanici_sorusu}
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}]
)

sql_sorgusu = response.choices[0].message.content.strip()
print("\n--- Model'in ürettiği SQL ---")
print(sql_sorgusu)

# --- 4. SQL'i çalıştır ---
try:
    cursor.execute(sql_sorgusu)
    sonuclar = cursor.fetchall()
    print("\n--- Sonuç ---")
    for satir in sonuclar:
        print(satir)
except Exception as hata:
    print(f"\nHata: {hata}")

cursor.close()
baglanti.close()