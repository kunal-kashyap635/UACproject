🏥 System Capacity & Care Load Analytics for Unaccompanied Children

📌 Project Overview

This project delivers a production-oriented analytics framework for monitoring and forecasting the operational capacity of the Unaccompanied Alien Children (UAC) care system.

The system functions as a dynamic care pipeline involving:

Intake into CBP custody

Transfer to HHS facilities

Medical and welfare support

Discharge and reunification with sponsors

The goal of this project is to transform raw daily operational data into actionable capacity intelligence that supports proactive decision-making and humanitarian planning.

🎯 Problem Statement

Although daily operational data is collected, there is no centralized analytical framework to continuously assess:

Total care system load

Balance between inflow and outflow

Capacity stress and relief periods

Sustainability of care delivery over time

Without structured analytics, decision-making becomes reactive, increasing the risk of overcrowding and strain on healthcare infrastructure.

🚀 Key Objectives

Primary Objectives

Quantify daily and cumulative care load across CBP and HHS

Identify periods of sustained capacity strain

Analyze balance between intake, transfers, and discharges

Secondary Objectives

Support staffing and shelter planning

Improve situational awareness

Enable data-driven humanitarian evaluation

📊 Dataset Description

| Column                                         | Description           |
| ---------------------------------------------- | --------------------- |
| Date                                           | Reporting date        |
| Children apprehended and placed in CBP custody | Daily intake volume   |
| Children in CBP custody                        | Active CBP load       |
| Children transferred out of CBP custody        | Flow into HHS         |
| Children in HHS Care                           | Active HHS load       |
| Children discharged from HHS Care              | Successful placements |

🧠 Analytical Framework

The project is structured into four layers:

1️⃣ Data Validation Layer

Missing date detection

Duplicate date checks

Logical constraint validation

Transfers ≤ CBP custody

Discharges ≤ HHS care

Anomaly flagging (no silent deletions)

2️⃣ Feature Engineering Layer

Derived metrics include:

Total System Load
CBP Custody + HHS Care

Net Daily Intake
Transfers − Discharges

Care Load Growth Rate
Day-over-day percentage change

Backlog Indicator
Sustained positive net intake

Discharge Offset Ratio
Ability to relieve incoming pressure

3️⃣ Trend & Stress Analysis

7-day and 14-day rolling averages

Volatility analysis (rolling standard deviation)

Capacity stress window detection

Stress windows identify sustained operational pressure beyond daily noise.

4️⃣ Forecasting (Time Series)

Two models were implemented:

🔹 ARIMA

Statistical baseline model

Captures autoregressive behavior

Handles trend via differencing

Model performance evaluated using:

* MAE

* RMSE

* MAPE

🖥️ Streamlit Dashboard

An interactive dashboard was built to provide real-time monitoring:

Features:

Date range filtering

Configurable rolling windows

KPI summary cards

Interactive Plotly visualizations

Capacity stress visualization

Net intake pressure tracking


## 🏗️ Project Architecture

```
uac-care-capacity-analytics/
│
├── data/
│   ├── raw/
│   │   └── uac_daily_data.csv
│   │
│   └── processed/
│       ├── validated_uac_data.csv
│       └── clean_uac_data.csv
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_validation.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_trend_pressure_analysis.ipynb
│   └── 05_forecasting_arima_prophet.ipynb
│
├── src/
│   ├── data_loader.py
│   ├── data_validation.py
│   ├── metrics.py
│   └── trends.py
│
├── app/
│   └── streamlit_app.py
│
├── requirements.txt
└── README.md
```

⚙️ Installation

git clone <repository-url>
cd uac-care-capacity-analytics

pip install -r requirements.txt

▶ Running the Dashboard

streamlit run app/streamlit_app.py

📈 Forecasting Notebook

notebooks/05_forecasting_arima.ipynb

📌 Design Philosophy

Strict separation of raw and processed data

Notebook experimentation → production modularization

Dynamic rolling analytics computed at runtime

Chronological train-test splitting for forecasting

No hardcoded business logic

💡 Key Insights

Sustained positive net intake leads to backlog accumulation

Rolling averages reveal structural stress not visible in daily fluctuations

Forecasting enables proactive staffing and shelter planning

Stress window detection provides policy-level early warning signals

👨‍💻 Author

Kunal Kashyap
Machine Learning Engineering
Research Paper : https://zenodo.org/records/19152300
