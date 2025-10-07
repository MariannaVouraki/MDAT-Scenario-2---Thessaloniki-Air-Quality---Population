# Scenario 2: Air Quality & Population Exposure in Thessaloniki

## Context
This scenario investigates the **relationship between atmospheric pollution** and the **resident population** across the **municipal districts of Thessaloniki**.  
It aims to evaluate **environmental exposure per capita** and identify **areas of higher pollution burden** using publicly available air-quality and census data.

It combines:
- **Dataset 1:** Air Quality Measurements from the Municipal Network of Thessaloniki (2010–2013)  
  *(GR – Μετρήσεις Ατμοσφαιρικής Ρύπανσης Δημοτικού Δικτύου 2010–2013)*  
- **Dataset 2:** Resident Population by Municipal Community (Census 2011)  
  *(GR – Μόνιμος Πληθυσμός ανά Δημοτική Κοινότητα, Απογραφή 2011)*

---

## Roles (Ontology)

- **Data Provider**: Supplies official datasets for air quality and population statistics.  
  (Municipality of Thessaloniki, Hellenic Statistical Authority)

- **Data Analyst**: Processes and merges data, executes Python workflows, and produces indicators.  
  (Implements normalization, WHO/EU limit checks, and per capita ratios.)

- **Researcher**: Interprets results, assesses urban exposure risk, and connects findings to environmental policy.  

---

## Workflow

1. **Data Provision**  
   The Data Provider supplies:
   - Air pollution datasets (multi-sheet Excel with pollutant concentrations per station).
   - Population data per municipal community.

2. **Data Processing**  
   The Data Analyst:
   - Normalizes and merges station data with population information.  
   - Computes mean pollutant concentrations per station and per pollutant (2010–2013).  
   - Maps stations to municipal districts using spatial correspondence.  
   - Calculates normalized exposure values (% of WHO/EU limits).  
   - Derives *Air Pollution Index per Capita (API_pc)* as a composite indicator.  
   - Generates analytical Excel outputs and visualizations.

3. **Evaluation**  
   The Researcher:
   - Reviews exceedances relative to WHO/EU thresholds.  
   - Interprets per capita results as indicators of population-weighted exposure.  
   - Identifies areas with elevated environmental stress and supports data-driven policy insights.

---

## Outputs

### Excel
`output/atmospheric_analysis_thessaloniki.xlsx`
- **Mapping** → Station to district correspondence  
- **Συνολικοί Μέσοι & Ανά Κάτοικο** →  
  Mean pollutant concentrations (2010–2013), population, pollutant per capita, WHO/EU compliance

### Visualizations
Generated automatically in `/output/`:
- `CO_by_district.png`  
- `NO2_by_district.png`  
- `O3_by_district.png`  
- `PM10_by_district.png`  
- `PM2.5_by_district.png`  
- `SO2_by_district.png`  
- `Total_Pollutants_per_Capita.png` → total pollution burden per inhabitant

---

## Indicators

| Indicator | Description | Unit |
|------------|--------------|------|
| Mean Concentration | Average pollutant concentration (2010–2013) | μg/m³ or mg/m³ |
| WHO/EU Limit | Official threshold value | μg/m³ or mg/m³ |
| Compliance | Within or above WHO/EU limits | text |
| Pollution per Capita | Mean concentration ÷ population | (μg/m³)/person |

---

## Purpose & Policy Relevance
This scenario demonstrates how open environmental and demographic datasets can be integrated to:
- Evaluate **urban air quality exposure** on a per capita basis.  
- Support **targeted environmental interventions**.  
- Contribute to **evidence-based municipal decision-making**

---

## Acknowledgments
Developed under the **MDAT** pilot,  
within the framework of the **UPcast**. 

License: CC BY-NC 4.0
