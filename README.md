# Heart Attack Analytics Dashboard

## Opis projekta

Heart Attack Analytics Dashboard je web aplikacija razvijena u sklopu projekta iz kolegija koja omogućuje analizu podataka o kardiovaskularnim bolestima te predviđanje rizika od srčanog udara primjenom modela strojnog učenja i dubokog učenja.

Projekt se sastoji od backend dijela razvijenog u FastAPI frameworku te frontend dijela izrađenog pomoću Vue.js i Vuetify biblioteke.

---

## Funkcionalnosti

* Prikaz osnovnih statističkih pokazatelja (KPI)
* Prikaz rezultata eksplorativne analize podataka (EDA)
* Vizualizacija EDA grafova
* Predviđanje rizika od srčanog udara
* Usporedba Random Forest i Deep Learning modela
* Grafički prikaz rezultata predikcije

---

## Tehnologije

### Backend

* Python
* FastAPI
* Pandas
* NumPy
* Scikit-learn
* TensorFlow / Keras
* Joblib

### Frontend

* Vue 3
* Vuetify
* Axios
* Chart.js
* Vite

---


## Pokretanje projekta

### Backend

Ući u mapu `backend`:

```bash
cd backend
```

Instalirati potrebne biblioteke:

```bash
pip install -r requirements.txt
```

Pokrenuti FastAPI server:

```bash
python -m uvicorn main:app --reload --port 8000
```

Backend će biti dostupan na:

```
http://127.0.0.1:8000
```

---

### Frontend

Ući u mapu `frontend`:

```bash
cd frontend
```

Instalirati ovisnosti:

```bash
npm install
```

Pokrenuti razvojni server:

```bash
npm run dev
```

Frontend će biti dostupan na:

```
http://localhost:5173
```

---

## API rute

GET /health  
GET /kpis    
GET /metrics  
GET /plots    
POST /predict

---

## Modeli strojnog učenja

Projekt koristi dva modela:

* Random Forest
* Deep Learning Neural Network

Konačni rezultat dobiva se kombiniranjem predikcija oba modela.
