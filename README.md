# Gans_E-Scooter_Data_Pipeline.
This project combines static demographic data (Wikipedia) with live weather and flight APIs (OpenWeather and AeroDataBox) to forecast Gans' e-scooter demand and optimize fleet rebalancing.By blending static demographics with live weather and flight data, this tool helps Gans predict e-scooter demand and deploy their fleet efficiently.

# 🛵 Gans E-Scooter Data Pipeline

An automated, end-to-end **Data Acquisition and ETL Pipeline** built for **Gans**—a fictional electric scooter sharing startup operating across major hubs.

---

## 📌 Project Overview

Electric scooter usage is highly dynamic and strongly influenced by external environmental factors and urban mobility trends. For an e-scooter company like **Gans**, operational efficiency depends on having scooters available where and when users actually need them. 

This project simulates a cloud-ready data acquisition pipeline that continuously collects, transforms, and loads external data—including baseline city demographics, real-time weather forecasts, and airport flight arrivals—into a centralized **MySQL relational database**. The aggregated data provides the foundation for downstream predictive models that optimize fleet distribution and rebalancing strategies.

---

## 🎯 Project Objectives

* **Automate External Data Collection**: Replace manual data gathering with an automated pipeline combining web scraping and REST API integrations.
* **Track Key Operational Signals**:
  * **Demographics**: Establish baseline population figures to gauge overall market size.
  * **Weather**: Capture temperature, precipitation, and wind speeds, as cold or rainy weather significantly drops scooter utilization.
  * **Inbound Passenger Flow**: Track flight arrivals at nearby airports to anticipate spikes in demand from arriving tourists and travelers.
* **Structured Data Architecture**: Design a normalized MySQL schema to reliably store both static reference data and time-series updates.
* **Modular Code Structure**: Organize the project into reusable modules and task-specific execution scripts defined by execution frequency (Interactive, Occasional, and Daily).

---

## 🏗️ Technical Architecture & Workflow

``` text
┌────────────────┐      ┌─────────────────────────┐      ┌──────────────────────┐
│  Data Sources  │ ───► │  Source Modules (src/)  │ ───► │   MySQL Database     │
├────────────────┤      ├─────────────────────────┤      ├──────────────────────┤
│ Wikipedia      │      │ collectors/wiki.py      │      │ cities               │
│ OpenWeather    │      │ collectors/weather.py   │      │ populations          │
│ AeroDataBox    │      │ collectors/aviation.py  │      │ forecasts            │
└────────────────┘      └─────────────────────────┘      │ airports & flights   │
                                                         └──────────────────────┘

---

## 🛠️ Tech Stack & Dependencies

Language: Python 3.x

Database: MySQL 8.0+

Data Processing: Pandas

Web Scraping: BeautifulSoup4, Requests

Database ORM: SQLAlchemy, PyMySQL

External APIs: OpenWeatherMap API, AeroDataBox API (via RapidAPI)

## 📁 Repository Structure

```text
├── src/
│   ├── collectors/
│   │   ├── wiki.py                  # Wikipedia scraping logic
│   │   └── weather.py               # OpenWeather API logic
│   └── utils/
│       └── helpers.py               # Utility and helper functions
├── config/
│   └── settings.py                  # Environment variables and API configurations
├── runnable_command/
│   ├── add_run_cities.py            # Entry point: Interactive setup to add new cities
│   ├── run_daily.py                 # Entry point: Daily automated weather & flight data pipeline
│   └── run_occasional.py            # Entry point: Occasional population and airport data updates
├── .env.example                     # Environment key template
├── .gitignore                       # Ensures secrets and local configs are not tracked
├── Gans_cities_schema.SQL           # Database setup and relational schema definitions
├── README.md                        # Documentation
└── requirements.txt                 # Project dependencies
