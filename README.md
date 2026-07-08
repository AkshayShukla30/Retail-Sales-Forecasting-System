# 📈 Retail Sales Forecasting & Demand Intelligence System

An end-to-end Retail Analytics project that predicts future product demand, detects sales anomalies, segments products based on demand behavior, and provides an interactive Streamlit dashboard for business decision-making.

The project combines statistical forecasting, machine learning, anomaly detection, clustering, and business analytics into a production-style workflow.
## 🌐 Live Demo

**Streamlit App:** https://retail-sales-forecasting-system.streamlit.app/

---
---

# 🚀 Features

- 📊 Interactive Sales Dashboard
- 📈 Time Series Forecasting (SARIMA, Prophet, XGBoost)
- 🚨 Sales Anomaly Detection (Isolation Forest & Z-Score)
- 📦 Product Demand Segmentation using K-Means
- 📉 Time Series Decomposition & Stationarity Analysis
- 📋 Business Insights & Forecast Reports
- 🌐 Interactive Streamlit Dashboard

---

# 🏗️ Project Architecture

```
Notebook
│
├── Data Cleaning
├── Feature Engineering
├── Exploratory Data Analysis
├── Time Series Analysis
├── SARIMA
├── Prophet
├── XGBoost
├── Anomaly Detection
├── Demand Segmentation
│
└── Generates
      │
      ▼
Models • Processed Data • Predictions • Reports
      │
      ▼
Streamlit Dashboard
```

---

# 📁 Project Structure

```
retail-sales-forecasting-system/

├── README.md

├── notebook/
│   ├── Retail_Sales_Forecasting.ipynb
│   ├── requirements.txt
│   └── data/
│       └── raw/
│           ├── train.csv
│           └── vgsales.csv

└── streamlit_app/
    ├── app.py
    ├── requirements.txt
    ├── assets/
    ├── models/
    ├── pages/
    ├── predictions/
    ├── processed/
    ├── reports/
    └── utils/
```

---

# 📊 Dashboard Pages

### 1️⃣ Sales Dashboard

- Sales KPIs
- Monthly Sales Trend
- Category Filter
- Region Filter
- Interactive Plotly Charts

---

### 2️⃣ Forecast Explorer

- Category & Region Selection
- Multi-Month Forecast
- Forecast Chart
- MAE & RMSE
- Forecast Download

---

### 3️⃣ Anomaly Detection

- Weekly Sales Visualization
- Isolation Forest
- Rolling Z-Score
- Business Reason for Every Anomaly

---

### 4️⃣ Demand Segmentation

- K-Means Clustering
- PCA Visualization
- Inventory Recommendations
- Demand Cluster Table

---

# 🛠 Tech Stack

### Programming

- Python

### Data Analysis

- Pandas
- NumPy

### Visualization

- Plotly
- Matplotlib

### Machine Learning

- Scikit-learn
- XGBoost

### Time Series

- Statsmodels
- Prophet

### Deployment

- Streamlit

---

# 📂 Dataset

### Primary Dataset

Superstore Sales Dataset

### Secondary Dataset

Video Game Sales Dataset

---

# ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>

cd retail-sales-forecasting-system
```

Create a Conda Environment

```bash
conda create -n retail python=3.11

conda activate retail
```

Install Notebook Dependencies

```bash
pip install -r notebook/requirements.txt
```

Install Streamlit Dependencies

```bash
pip install -r streamlit_app/requirements.txt
```

---

# ▶️ Running the Notebook

```bash
cd notebook

jupyter notebook
```

Run **Retail_Sales_Forecasting.ipynb** completely to generate:

- Processed Data
- Trained Models
- Forecast Files
- Reports

---

# 🌐 Running the Dashboard

```bash
cd streamlit_app

streamlit run app.py
```

---

# 🚀 Deployment

Deploy directly on Streamlit Community Cloud.

Main file:

```
streamlit_app/app.py
```

Requirements:

```
streamlit_app/requirements.txt
```

---

# 🔮 Future Improvements

- LSTM Forecasting
- Temporal Fusion Transformer (TFT)
- Holiday & Promotion Features
- FastAPI REST API
- Docker Support
- Automated Model Retraining
- CI/CD Pipeline

---

# 👨‍💻 Author

**Akshay Shukla**

- **LinkedIn:** https://www.linkedin.com/in/akshayshukla-/
- **GitHub:** https://github.com/AkshayShukla30

---

# 📬 Contact

- **Email:** akshayshukla466@gmail.com
