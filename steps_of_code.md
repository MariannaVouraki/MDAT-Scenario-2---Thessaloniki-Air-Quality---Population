## ⚙️ Thessaloniki Air Quality Workflow — Process Mapping

This section maps the analytical steps of the Python script  
(`final_script.py`) to semantic processes using the **Data Privacy Vocabulary (DPV 2.2)** and the **ODRL 2.2 Information Model**.

---

### 🧩 Step 1 — Read and Normalize Pollution Data
**Description:**  
Reads pollutant concentration data from the municipal monitoring Excel file and normalizes column names.  

**Code Functions:**  
`read_pollution_sheets()`, `normalize_columns()`

**DPV Process:** `dpv:Collect`, `dpv:Transform`, `dpv:Standardise`  
**ODRL Action:** `odrl:use`, `odrl:derive`  
**Actor:** Data Analyst

---

### 🧩 Step 2 — Read and Normalize Population Data
**Description:**  
Reads population data from the extended demographic dataset (`resident_population_census2011-extended thessaloniki.xlsx`) and standardizes community names.  

**Code Functions:**  
`read_population()`, `normalize_columns()`

**DPV Process:** `dpv:Collect`, `dpv:Transform`  
**ODRL Action:** `odrl:use`  
**Actor:** Data Analyst

---

### 🧩 Step 3 — Compute Mean Pollutant Concentrations
**Description:**  
Computes mean pollutant concentrations for each monitoring station over 2010–2013.  

**Code Function:**  
`compute_overall_means()`

**DPV Process:** `dpv:Aggregate`, `dpv:Derive`  
**ODRL Action:** `odrl:derive`  
**Actor:** Data Analyst

---

### 🧩 Step 4 — Map Stations to Administrative Areas
**Description:**  
Maps each monitoring station to its corresponding municipal district using predefined relationships.  

**Code Snippet:**  
`STATION_TO_AREA_ADMIN` dictionary + merge with population data  

**DPV Process:** `dpv:Combine`, `dpv:Transform`  
**ODRL Action:** `odrl:use`, `odrl:derive`  
**Actor:** Data Analyst

---

### 🧩 Step 5 — Calculate Pollution per Capita
**Description:**  
Divides mean pollutant values by district population to estimate pollution exposure per inhabitant.  

**Code Snippet:**  
`overall_means["Ρύποι ανά κάτοικο"] = ...`

**DPV Process:** `dpv:Derive`, `dpv:Aggregate`, `mdat:ExposureIndicator`  
**ODRL Action:** `odrl:derive`, `odrl:aggregate`  
**Actor:** Data Analyst

---

### 🧩 Step 6 — Evaluate Compliance with WHO/EU Limits
**Description:**  
Checks each pollutant against WHO/EU thresholds and labels as “within” or “exceeded”.  

**Code Function:**  
`check_pollutant_status()`

**DPV Process:** `dpv:Assess`, `dpv:EvaluateRisk`  
**ODRL Action:** `odrl:analyze`  
**Actor:** Data Analyst

---

### 🧩 Step 7 — Export Analytical Results
**Description:**  
Writes mapping and computed results to Excel output (`atmospheric_analysis_thessaloniki.xlsx`).  

**Code Snippet:**  
`pd.ExcelWriter(outxlsx)`  

**DPV Process:** `dpv:Store`, `dpv:Use`  
**ODRL Action:** `odrl:reproduce`  
**Actor:** Data Analyst

---

### 🧩 Step 8 — Generate Visualizations
**Description:**  
Creates graphs for pollutant levels per district and total pollution per capita.  

**Code Functions:**  
`plot_pollutant_by_district()`, `plot_total_pollution_per_capita()`

**DPV Process:** `dpv:Visualise`, `dpv:Use`  
**ODRL Action:** `odrl:display`, `odrl:reproduce`  
**Actor:** Data Analyst

---

### 🧩 Step 9 — Review and Interpret Results
**Description:**  
The Researcher interprets visual results and numerical outputs to identify areas with higher environmental stress.  

**DPV Process:** `dpv:Analyse`, `dpv:Report`, `mdat:DerivedIndicator`  
**ODRL Action:** `odrl:analyze`, `odrl:present`  
**Actor:** Researcher

---

### 🧩 Step 10 — Share Results under Open License
**Description:**  
The derived datasets and visualizations are published as open results under **CC BY-NC 4.0**, ensuring transparent reuse.  

**DPV Process:** `dpv:Share`, `dpv:Disclose`, `dpv:DerivedData`  
**ODRL Action:** `odrl:distribute`, `odrl:reproduce`  
**Actor:** Data Provider / Researcher

---

### ✅ Summary
The Python workflow operationalizes the scenario’s semantic model by:
- Integrating **open** and **restricted** datasets (D1–D3)  
- Deriving exposure indicators (D4)  
- Ensuring **traceability and policy alignment** through **DPV + ODRL** mappings
