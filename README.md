TODO: Brieflyb explain my pagination strategy and data enrichment logic

# Order Pipeline Project

## Overview
The **Order Pipeline Project** is a Python-based data processing and analysis system designed to retrieve, enrich, analyze, and export product and user data. This project leverages API data, Pandas for data manipulation, and JSON for output storage. It is structured to simulate an end-to-end analytics pipeline.

The primary goal of this project is to demonstrate a clean, modular approach to data processing, suitable for testing and extension.

---

## Project Structure

```
pipeline/
├── init.py
├── pipeline.py # Main pipeline class to run the full workflow
├── api_client.py # Handles fetching data from APIs
├── data_enricher.py # Converts and merges API data into enriched DataFrames
├── data_analyzer.py # Performs analysis on the enriched data
├── exporter.py # Exports analysis results to JSON
├── config.py # Configuration management
tests/
├── test_pipeline.py
├── test_api_client.py
├── test_data_enricher.py
├── test_data_analyzer.py
├── test_exporter.py
└── test_config.py
main.py #Entry Point to my pipeline
README.md
```

---

## Features

1. **Data Retrieval**  
   Fetches products and users from APIs using `APIClient`. The APIClient implements a pagination logic that makes on request to the `/products` api and stores the data. This data is now used to simulate pagination using slicing vai the limits

2. **Data Enrichment**  
   Converts API responses into Pandas DataFrames and merges them on user IDs to enrich product data with seller information, including username, email, and name. Calculates total revenue for each product.

3. **Data Analysis**  
   Performs key metrics calculations such as total products per seller, total revenue, and average price per seller.

4. **Exporting**  
   Exports analysis results into JSON files for easy storage and sharing.

5. **Configuration Management**  
   Centralized configuration file handling using `ConfigManager` to manage project settings.

---

## Pipeline Workflow

The pipeline follows a modular, step-by-step process to fetch, enrich, analyze, and export data.
```
ConfigManager : Loads the configuration from the `popeline.cfg` file
│
▼
APIClient
│
▼
Fetch Products & Users. Uses the configuration settings loaded in be the configmanager
│
▼
DataEnricher
├─ Convert products to DataFrame
├─ Convert users to DataFrame
├─ Merge products & users on user ID
└─ Calculate revenue per product
│
▼
Analyzer
├─ Total products per seller
├─ Total revenue per seller
├─ Average price per seller
└─ Generate analysis dictionary
│
▼
Exporter
└─ Export analysis results to JSON
```
**Step-by-Step Description:**

* APIClient: Fetches product and user data from the API.

* DataEnricher: Converts raw JSON to DataFrames, merges datasets on user ID, and calculates revenue for each product.

* Analyzer: Computes key metrics for reporting.

* Exporter: Saves the results into a JSON file for further use.


## Installation

1. Clone the repository:
```bash
git clone git@github.com:king-obobo/de-week4-advancedpipeline-Ebuka-Obobo.git
cd order-pipeline
```

2. Create a virtual environment and activate it
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Install uv
```
pip install uv
```
4. Install dependencies using uv
```
uv sync
```

## Usage
Run the full pipeline. In the roor folder, run the `main.py` file:
```
uv run main.py
```

## Testing
This project uses pytest for unit testing. Tests cover API fetching, data enrichment, analysis, and export functionality.

Run tests with:
```
pytest -v
```