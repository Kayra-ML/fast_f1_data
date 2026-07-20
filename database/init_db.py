import os
from sqlalchemy import text
from sqlalchemy import create_engine

# Railway bağlantı adresiniz (Hardcoded)
DB_URL = "postgresql://postgres:qFMUkSMAoKakangFgvKXgoLpjjhUuWHM@hayabusa.proxy.rlwy.net:34011/railway"


def init_database():
    print("Railway veritabanına bağlanılıyor...")
    engine = create_engine(DB_URL)
    
    schema_path = "schema.sql"
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"{schema_path} bulunamadı!")

    print(f"'{schema_path}' dosyası okunuyor...")
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    print("Tablolar Railway veritabanında oluşturuluyor...")
    
    with engine.begin() as conn:  # begin() otomatik commit yapar
        # Birden fazla SQL sorgusunu güvenle çalıştırmak için tek tek çalıştırıyoruz
        # Yorum satırlarını ve boşlukları atla
        queries = [q.strip() for q in sql_script.split(';') if q.strip()]
        for query in queries:
            conn.execute(text(query))
            
    print("Tüm tablolar başarıyla oluşturuldu! Veritabanı veri aktarımına hazır.")

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
