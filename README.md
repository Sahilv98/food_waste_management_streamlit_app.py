# 🍽️ Local Food Wastage Management System

## 📌 Project Overview
Food wastage is a critical global challenge. While restaurants and supermarkets routinely discard surplus food, countless individuals and organizations face food insecurity. The **Local Food Wastage Management System** is a data-driven platform built to bridge this gap by connecting surplus food providers directly with local receivers (NGOs, shelters, and charities). 

This project features a fully interactive **Streamlit application** backed by an **SQLite database**, designed to facilitate real-time food tracking, manage donation claims, and provide deep analytical insights into local food waste patterns to optimize hyper-local logistics.

## ✨ Key Features
* **Interactive Dashboard:** A dynamic Streamlit-powered UI for seamless data exploration and platform management.
* **Complete CRUD Operations:** Easily add, view, update, and remove surplus food listings and donation claims.
* **Advanced SQL Analytics:** 15+ integrated SQL queries that identify top contributors, high-demand areas, and fulfillment bottlenecks.
* **Exploratory Data Analysis (EDA):** Visual insights into food expiry trends, batch size distributions, and stakeholder ecosystems.
* **Hyper-Local Matching:** Geolocation and contact tracking designed to ensure rapid fulfillment before razor-thin food expiry windows close.

## 🛠️ Tech Stack
* **Language:** Python
* **App Framework:** Streamlit
* **Database:** SQLite 
* **Data Analysis:** Pandas
* **Data Visualization:** Matplotlib, Seaborn

## 📂 Core Datasets
The system operates on four interconnected datasets that track the full lifecycle of a food donation:
1. `providers_data.csv` - Supplier details, categories, and locations.
2. `receivers_data.csv` - NGO, charity, and individual claimant profiles.
3. `food_listings_data.csv` - Available food batches, dietary types, and strict expiry dates.
4. `claims_data.csv` - Real-time tracking of Pending, Completed, and Cancelled food claims.
