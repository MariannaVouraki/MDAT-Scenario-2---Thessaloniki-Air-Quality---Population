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
During the analytical phase, the **Researcher** found that the initial population dataset did not provide the required **spatial resolution** to correctly associate population figures with individual air-quality stations.  
To ensure accurate exposure analysis, the Researcher initiated a **data negotiation process** with the **Data Provider**.

Through this negotiation:
1. The **Researcher** justified the scientific need for finer-grained demographic data at the sub-municipal level.  
2. The **Data Provider**, acting as custodian of the dataset, reviewed the request and applied a **graded-access policy**, defining terms of controlled reuse, privacy protection, and citation.  
3. Upon agreement, the **Data Provider** granted the Researcher access to an **extended dataset** titled  
   **`resident_population_census2011-extended thessaloniki.xlsx`**,  
   containing more detailed demographic segmentation aligned with the municipal sub-divisions.

---

## Roles (Ontology Alignment)

| Role | Description | Ontology Class |
|------|--------------|----------------|
| **Data Provider** | Governs official datasets, defines access policies, and manages data-sharing negotiations. | `dpv:DataController`, `dpv:Authority`, `dpv:AccessControlMethod` |
| **Researcher** | Requests access to restricted datasets and interprets analytical results for policy insights. | `dpv:Recipient` (Purpose: `dpv:ResearchAndDevelopment`), `odrl:assignee` |
| **Data Analyst** | Performs transformations, aggregation, and visualization using Python scripts. | `dpv:DataProcessor`, `odrl:operator` |

---

## Ontological Consistency Notes

- All **DPV terms** are verified against [DPV 2.2](https://w3id.org/dpv/2.2/dpv#).  
- All **ODRL actions** are taken from the official [ODRL Core Vocabulary](https://www.w3.org/ns/odrl/2/).  
- Policy negotiation (Step 1) is represented conceptually via `dpv:AuthorisationProcedure` and `dpv:NegotiateContract`.  
- Analytical and reporting steps (7–9) correctly use `odrl:analyze`, `odrl:present`, and `dpv:Analyse`.  
- The mapping ensures **semantic interoperability** and **policy traceability** within the MDAT framework.

---

## Datasets (Ontology Classification)

| ID | Title | Category | Base DPV Type | License | Access |
|----|--------|-----------|---------------|----------|--------|
| D1 | `metriseis_atmosfairikis_rypansis_dimotikoy_diktyoy_2010_2013.xlsx` | `mdat:EnvironmentalData` | `dpv:NonPersonalData` | ODbL 1.0 | Public |
| D2 | `resident_population_census2011_Thessaloniki_metropolitan.xlsx` | `mdat:DemographicData` | `dpv:NonPersonalData` | ODbL 1.0 | Public |
| D3 | `resident_population_census2011-extended thessaloniki.xlsx` | `mdat:DemographicData`, `dpv:RestrictedData`, `mdat:ExtendedPopulationData` | `dpv:NonPersonalData` | Controlled Access | Negotiated |
| D4 | `atmospheric_analysis_thessaloniki.xlsx`, PNG graphs | `dpv:DerivedData`, `mdat:ExposureIndicator` | `dpv:NonPersonalData` | CC BY-NC 4.0 | Open Results |

---

# Workflow (Mapped to DPV & ODRL)

| Step | Description | DPV Process | ODRL Action | Actor |
|------|--------------|--------------|--------------|--------|
| 1 | Negotiate and authorize access to D3 (extended dataset). | `dpv:Access`, `dpv:AccessControlMethod`, `dpv:AuthorisationProcedure`, `dpv:NegotiateContract` | *(policy-level negotiation, no direct ODRL action)* | Data Provider ↔ Researcher |
| 2 | Collect open environmental data (pollution readings). | `dpv:Collect`, `dpv:Access`, `mdat:EnvironmentalData` | `odrl:use` | Data Analyst |
| 3 | Collect demographic data (extended version). | `dpv:Collect`, `dpv:Access`, `mdat:DemographicData`, `dpv:RestrictedData` | `odrl:use` | Data Analyst |
| 4 | Clean and normalize both datasets (remove inconsistencies, harmonize units). | `dpv:Transform`, `dpv:Standardise` | `odrl:derive` | Data Analyst |
| 5 | Aggregate and compute mean pollutant levels (2010–2013). | `dpv:Aggregate`, `dpv:Derive` | `odrl:derive` | Data Analyst |
| 6 | Merge datasets and compute pollutant-per-capita ratios. | `dpv:Combine`, `dpv:Aggregate`, `dpv:Derive` | `odrl:aggregate` | Data Analyst |
| 7 | Assess compliance with WHO/EU limits. | `dpv:Assess`, `dpv:EvaluateRisk` | `odrl:analyze` | Data Analyst |
| 8 | Generate graphs and visual summaries. | `dpv:Visualise`, `dpv:Use` | `odrl:display`, `odrl:reproduce` | Data Analyst |
| 9 | Interpret and report per-capita exposure findings. | `dpv:Analyse`, `dpv:Report` | `odrl:present` | Researcher |
| 10 | Share derived data and visualizations under open license. | `dpv:Share`, `dpv:Disclose`, `dpv:DerivedData` | `odrl:distribute` | Data Provider / Researcher |

---

# Ontology Action Mapping Array (Execution Order Aligned)

| Element / Description | DPV Term | ODRL Term | Proposed Custom Term (`mdat:`) | Notes / Usage |
|------------------------|-----------|------------|--------------------------------|----------------|
| **Negotiate and authorize access** | `dpv:Access`, `dpv:AccessControlMethod`, `dpv:AuthorisationProcedure`, `dpv:NegotiateContract` | *(policy-level)* | `mdat:NegotiatedAccessPolicy` | Formal graded-access agreement between provider and researcher. |
| **Load air-quality and population datasets** | `dpv:Collect`, `dpv:Access` | `odrl:use` |  | Read Excel datasets for analysis. |
| **Normalize and clean data** | `dpv:Transform`, `dpv:Standardise` | `odrl:derive` |  | Harmonize fields and measurement units. |
| **Compute mean pollutant concentrations** | `dpv:Aggregate`, `dpv:Derive` | `odrl:derive` | `mdat:CalculateMeanPollutant` | Calculate 2010–2013 averages per monitoring station. |
| **Map stations to districts** | `dpv:Combine`, `dpv:Transform` | `odrl:aggregate` | `mdat:StationDistrictMapping` | Associate stations with municipal districts. |
| **Calculate pollution per capita** | `dpv:Aggregate`, `dpv:Derive` | `odrl:aggregate` | `mdat:ExposureIndicator` | Compute pollutant exposure per inhabitant. |
| **Evaluate compliance with WHO/EU limits** | `dpv:Assess`, `dpv:EvaluateRisk` | `odrl:analyze` | `mdat:PollutantLimitCheck` | Determine exceedances of reference limits. |
| **Store analytical results** | `dpv:Store`, `dpv:Use` | `odrl:reproduce` |  | Export Excel outputs. |
| **Generate visualizations** | `dpv:Visualise`, `dpv:Use` | `odrl:display`, `odrl:reproduce` |  | Create graphs for pollutants and exposure. |
| **Interpret and report results** | `dpv:Analyse`, `dpv:Report` | `odrl:present` | `mdat:DerivedIndicator` | Evaluate per-capita impact and interpret results. |
| **Share derived data and visuals** | `dpv:Share`, `dpv:Disclose`, `dpv:DerivedData` | `odrl:distribute` |  | Publish open outputs under CC BY-NC 4.0. |

---

## Indicators

| Indicator | Description | DPV Class | Unit |
|------------|--------------|------------|------|
| Mean Concentration | Average pollutant concentration (2010–2013) | `mdat:PollutantMean` | μg/m³ or mg/m³ |
| WHO/EU Limit | Official reference threshold | `mdat:PollutantLimit` | μg/m³ or mg/m³ |
| Compliance | Whether measurement exceeds legal threshold | `dpv:ComplianceStatus` | text |
| Pollution per Capita | Mean pollutant value divided by population | `mdat:ExposureIndicator` | (μg/m³)/person |

---

### Domain-Specific Concepts (MDAT)

| Concept | Description |
|----------|--------------|
| `mdat:AirPollutant` | Represents a measurable pollutant (SO₂, NO₂, PM₂.₅, etc.). |
| `mdat:MonitoringStation` | Physical location of air-quality data collection. |
| `mdat:EnvironmentalData` | Non-personal dataset of air-pollutant measurements. |
| `mdat:DemographicData` | Aggregated population or community-level dataset. |
| `mdat:ExtendedPopulationData` | High-resolution demographic dataset shared under negotiated access. |
| `mdat:ExposureIndicator` | Pollutant load per inhabitant (μg/m³/person). |
| `mdat:AirPollutionIndex` | Composite indicator summarizing total exposure per capita. |
| `mdat:DerivedIndicator` | Output metric derived from environmental and demographic data. |
| `mdat:NegotiatedAccessPolicy` | Policy describing graded access and reuse conditions between provider and researcher. |

---

## Purpose & Policy Relevance
This scenario demonstrates how **open and controlled-access datasets** can be semantically integrated under **DPV and ODRL governance models** to:
- Quantify **urban air-quality exposure** at district and per-capita levels.  
- Illustrate the **negotiation and graded-access process** within data spaces.  
- Support **transparent, policy-relevant environmental assessments** in line with the **MDAT Pilot** objectives.  

---

## Acknowledgments
Developed under the **MDAT** pilot,  
within the framework of the **UPcast** project.  

Ontologies used:  
`DPV 2.2`, `ODRL 2.2`, `DPV-PD`, `MDAT domain extension`.  

**License:** CC BY-NC 4.0
