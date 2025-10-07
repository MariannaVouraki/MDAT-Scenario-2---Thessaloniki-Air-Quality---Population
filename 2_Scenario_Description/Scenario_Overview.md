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

## Negotiation & Graded Access

During the analytical phase, the **Researcher** determined that the initial population dataset did not provide the required **spatial resolution** to correctly associate population figures with individual air-quality stations.  
To ensure accurate exposure analysis, the Researcher initiated a **data negotiation process** with the **Data Provider**.

Through this negotiation:
1. The **Researcher** justified the scientific need for finer-grained demographic data at the sub-municipal level (sub-departments of the Metropolitan Area of Thessaloniki).  
2. The **Data Provider**, acting as the custodian of the demographic dataset, reviewed the request and applied a **graded access policy**, defining terms of controlled reuse, privacy protection, and citation.  
3. Upon agreement, the **Data Provider** granted the Researcher access to an **extended dataset** titled  
   **“resident_population_census2011-extended thessaloniki.xlsx”**,  
   containing more detailed demographic segmentation aligned with the municipal sub-divisions.

This negotiation illustrates the **governance and access-management dimension** of data spaces, where collaboration and trust enable the controlled sharing of higher-resolution data for legitimate analytical purposes.

---

## Roles (Ontology)

- **Data Provider**: Supplies and governs official datasets for air quality and population statistics, defines graded-access policies, and negotiates dataset extensions.  
  (Municipality of Thessaloniki, Hellenic Statistical Authority)

- **Data Analyst**: Processes and merges data, executes Python workflows, and produces indicators.  
  (Implements normalization, WHO/EU limit checks, and per-capita ratios.)

- **Researcher**: Requests and uses datasets under agreed access policies, interprets results, and connects findings to environmental policy.

---

## Workflow

1. **Data Provision & Negotiation**  
   - Initial datasets are supplied as open data.  
   - A negotiation occurs to enable access to the extended population dataset under a graded access policy.

2. **Data Processing**  
   The Data Analyst:
   - Normalizes and merges pollution and extended population data.  
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
This scenario demonstrates how open environmental and demographic datasets can be integrated — and, when necessary, **negotiated under graded-access policies** — to:
- Evaluate **urban air quality exposure** on a per capita basis.  
- Support **targeted environmental interventions**.  
- Contribute to **evidence-based municipal decision-making** while respecting **data-governance principles**.

---

## Acknowledgments
Developed under the **MDAT** pilot,  
within the framework of **UPcast**.

License: CC BY-NC 4.0
