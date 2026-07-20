<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:e11d48,100:dc2626&height=200&section=header&text=F1+Data+Analysis&fontSize=58&fontColor=ffffff&fontAlignY=38&desc=Formula+1+Verisi+Üzerine+Full-Stack+Analiz+Platformu&descAlignY=58&descAlign=50&animation=fadeIn" />

</div>

> **"Veriden pist stratejisi oku."**  
> 2024-2025 Formula 1 sezonlarını kapsayan, PostgreSQL tabanlı büyük veri analizi yapan, RAM-verimli sorgu mimarisi ile tasarlanmış web platformu.

---

## 💡 Fikir ve Motivasyon

F1 büyük veri problemidir. Her yarış yüzlerce sürücü verisi, binlerce tur zamanı, pit stop stratejileri, DNF oranları... Bunları anlamlı grafiklerle görmek istedim.

**Temel tasarım kararı:** Tüm veriyi çekmek yerine, frontend filtreleme + backend pagination + UNION ALL sorgu stratejisi. Böylece milyonlarca satır veri olsa bile uygulama hızlı kalıyor.

---

## 🏗️ Mimari

```
Frontend (React + TypeScript + Vite)
    ↓ Filtre parametreleri
FastAPI Backend (Python)
    ↓ Parameterize SQL + UNION ALL
PostgreSQL (Railway)
    ├── results_2024
    ├── results_2025
    ├── lap_times_2024
    ├── lap_times_2025
    └── ...
```

**RAM-Verimli Sorgu Mimarisi:**
```python
class F1AnalysisService:
    # Yıl bazında UNION ALL sorguları
    # Pagination (limit/offset)
    # Parameterized queries (SQL injection güvenli)
    # SQLAlchemy connection pooling
```

---

## ⚙️ Analiz Modülleri

### 🏎️ Sürücü Analizi
- **Performans Sıralaması** — kazanma, podyum, DNF oranı
- **Tur Süresi Analizi** — en iyi tur, ortalama, tutarlılık
- **Yarış Bazında Karşılaştırma** — sürücüler arası

### 🏭 Takım / Constructor Analizi
- Takım puan gelişimi (sezon boyunca)
- Takım güvenilirlik skoru
- Sürücü çift performans karşılaştırması

### 🗓️ Sezon Görünümü
- 2024-2025 sezon verileri
- Pist bazında analizler
- Hava koşulu etkisi

---

## 🛠️ Tech Stack

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python, FastAPI |
| ORM / SQL | SQLAlchemy, Ham SQL (UNION ALL) |
| Veritabanı | PostgreSQL (Railway) |
| Frontend | React 19, TypeScript, Vite |
| Stil | TailwindCSS |
| Veri Güvenliği | Parameterized queries |

---

## 📁 Proje Yapısı

```
f1DataAnalysis/
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py                  # FastAPI + health check
│       ├── routes/
│       │   └── analysis.py          # API endpoint'leri
│       └── services/
│           ├── f1_analysis_service.py  # Ana analiz motoru (510 satır)
│           └── analysis_service.py    # Yardımcı sorgular
├── frontend/
│   └── src/                         # React + TypeScript UI
├── database/                        # SQL şemaları ve seed
├── docs/                            # Teknik dokümantasyon
└── test_backend.py                  # Backend test suite
```

---

## 🚀 Kurulum

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# DATABASE_URL=postgresql://...
uvicorn app.main:app --reload
# → http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

---

## 🔗 API Endpoint'leri

| Endpoint | Açıklama |
|----------|----------|
| `GET /` | API durum kontrolü |
| `GET /health` | PostgreSQL bağlantı testi |
| `GET /analysis/drivers` | Sürücü performans sıralaması |
| `GET /analysis/constructors` | Takım analizi |
| `GET /analysis/laps` | Tur süresi verileri |

---

## 📊 Veri Güvenliği

Tüm SQL sorguları parameterized (hazırlanmış ifadeler) kullanır:
```python
# ✅ Güvenli
conn.execute(text("SELECT * FROM results WHERE driver = :driver_id"), 
             {"driver_id": driver_id})

# ❌ ASLA
f"SELECT * FROM results WHERE driver = '{driver_id}'"
```

---

<div align="center">
<img src="https://img.shields.io/badge/FastAPI-Python-009688?style=flat-square&logo=fastapi" />
<img src="https://img.shields.io/badge/PostgreSQL-Database-316192?style=flat-square&logo=postgresql" />
<img src="https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react" />
<img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat-square" />
<img src="https://img.shields.io/badge/F1-2024--2025-E10600?style=flat-square" />

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:dc2626,50:e11d48,100:0d1117&height=100&section=footer" />
</div>
