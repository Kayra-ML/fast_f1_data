import os
import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

# Railway bağlantı adresiniz (Hardcoded Public URL)
DB_URL = "postgresql://postgres:qFMUkSMAoKakangFgvKXgoLpjjhUuWHM@hayabusa.proxy.rlwy.net:34011/railway"

# SQLAlchemy Engine oluştur
engine = create_engine(DB_URL)

DATA_DIR = "f1_data"
YEARS = [2024, 2025]

def bulk_upsert(df, table_name, engine, primary_keys):
    if df.empty:
        return
    
    # DataFrame'i dictionary listesine çevir
    data_dicts = df.to_dict(orient='records')
    
    # Tüm NaN ve NaT değerlerini Python None (SQL NULL) değerine zorla
    for row in data_dicts:
        for k, v in row.items():
            if pd.isna(v) or v == "nan" or v == "":
                row[k] = None

    
    from sqlalchemy import Table, MetaData
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    
    stmt = insert(table).values(data_dicts)
    
    update_dict = {c.name: c for c in stmt.excluded if c.name not in primary_keys}
    
    if update_dict:
        stmt = stmt.on_conflict_do_update(
            index_elements=primary_keys,
            set_=update_dict
        )
    else:
        stmt = stmt.on_conflict_do_nothing(index_elements=primary_keys)

    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()


def load_drivers():
    print("Suruculer (Drivers) yukleniyor...")
    all_drivers = []
    
    for year in YEARS:
        file_path = os.path.join(DATA_DIR, str(year), f"drivers_{year}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_drivers.extend(data)
                
    if not all_drivers:
        print("Surucu verisi bulunamadi.")
        return

    df = pd.DataFrame(all_drivers)
    
    df = df.rename(columns={
        "driverId": "driver_id",
        "permanentNumber": "permanent_number",
        "givenName": "given_name",
        "familyName": "family_name",
        "dateOfBirth": "date_of_birth"
    })
    
    if 'url' in df.columns:
        df = df.drop(columns=['url'])
        
    if 'date_of_birth' in df.columns:
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')

    df = df.drop_duplicates(subset=['driver_id'])
    
    bulk_upsert(df, "drivers", engine, primary_keys=["driver_id"])
    print(f"Toplam {len(df)} surucu basariyla 'drivers' tablosuna aktarildi.")


def load_constructors():
    print("Takimlar (Constructors) yukleniyor...")
    all_constructors = []
    
    for year in YEARS:
        file_path = os.path.join(DATA_DIR, str(year), f"constructors_{year}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_constructors.extend(data)
                
    if not all_constructors:
        print("Takim verisi bulunamadi.")
        return

    df = pd.DataFrame(all_constructors)
    
    df = df.rename(columns={
        "constructorId": "constructor_id"
    })
    
    if 'url' in df.columns:
        df = df.drop(columns=['url'])

    df = df.drop_duplicates(subset=['constructor_id'])
    
    bulk_upsert(df, "constructors", engine, primary_keys=["constructor_id"])
    print(f"Toplam {len(df)} takim basariyla 'constructors' tablosuna aktarildi.")


def load_circuits():
    print("Pistler (Circuits) yukleniyor...")
    all_circuits = []
    
    for year in YEARS:
        file_path = os.path.join(DATA_DIR, str(year), f"circuits_{year}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_circuits.extend(data)
                
    if not all_circuits:
        print("Pist verisi bulunamadi.")
        return

    df = pd.DataFrame(all_circuits)
    
    if 'Location' in df.columns:
        locations = df['Location'].apply(pd.Series)
        df['lat'] = pd.to_numeric(locations['lat'], errors='coerce')
        df['lng'] = pd.to_numeric(locations['long'], errors='coerce')
        df['location'] = locations['locality']
        df['country'] = locations['country']
        df = df.drop(columns=['Location'])

    df = df.rename(columns={
        "circuitId": "circuit_id",
        "circuitName": "circuit_name"
    })
    
    if 'url' in df.columns:
        df = df.drop(columns=['url'])

    df = df.drop_duplicates(subset=['circuit_id'])
    
    bulk_upsert(df, "circuits", engine, primary_keys=["circuit_id"])
    print(f"Toplam {len(df)} pist basariyla 'circuits' tablosuna aktarildi.")


if __name__ == "__main__":
    print("=== F1 Veritabani Aktarim Botu (ETL) Basliyor ===")
    
    try:
        load_drivers()
        load_constructors()
        load_circuits()
        print("Sabit ana verilerin aktarimi basariyla tamamlandi!")
    except Exception as e:
        print(f"Bir hata olustu: {str(e)}")
