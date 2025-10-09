## 🔄 Workflow Overview

The workflow of **Scenario 2** integrates environmental and demographic data to assess air pollution exposure across the municipal districts of Thessaloniki.  
It consists of three main phases: **Data Negotiation**, **Processing & Analysis**, and **Evaluation & Visualization**.

---
## Workflow

### Data Provision
The **Data Provider** supplies:
- Air quality measurements from the Municipal Monitoring Network (2010–2013).  
- Population datasets from the 2011 Census (public version).  
- After negotiation, provides the **extended population dataset** with higher spatial resolution for the Thessaloniki Metropolitan Area.

### Data Processing
The **Data Analyst**:
- Normalizes and merges air-quality and population data.  
- Calculates mean pollutant concentrations per station (2010–2013).  
- Maps stations to corresponding municipal or sub-municipal units.  
- Computes pollutant-per-capita indicators and composite *Air Pollution Index per Capita (API_pc)*.  
- Generates analytical Excel outputs and visualizations (pollutant charts and total exposure graphs).

### Evaluation
The **Researcher**:
- Reviews pollutant levels against EU thresholds.  
- Interprets per-capita exposure and identifies areas with higher environmental stress.  
- Links findings to data-driven urban and environmental policy recommendations.

---

### Summary
The workflow demonstrates how **open data** and **restricted data** can be securely combined within a **data space governance model**.  
It ensures analytical accuracy while maintaining **data protection, provenance, and reuse transparency** through DPV and ODRL semantics.
