# Data Specification

## Dataset 1: Air Quality Measurements (2010–2013)
**Title:** Air Quality Measurements – Thessaloniki Municipal Monitoring Network (2010–2013)  
**Description:** Contains daily pollutant concentration measurements (SO₂, NO₂, NO, O₃, PM10, PM2.5, CO) from the municipal air-quality monitoring network of the City of Thessaloniki for the period 2010–2013. The dataset provides essential information for analyzing air pollution trends across the urban area.  
**Source:** (TDS) Thessaloniki Data Space [https://tds.okfn.gr/product/36]  
**Format:** Excel (.xlsx)  
**Key Fields:** date, station_name, pollutant, value  

---

## Dataset 2: Resident Population (Census 2011)
**Title:** Resident Population of Thessaloniki Municipality (Census 2011)  
**Description:** Contains population data per municipal community, based on the 2011 Population and Housing Census by ELSTAT. The dataset provides the official demographic reference used for calculating per-capita pollution exposure indicators.  
**Source:** (TDS) Thessaloniki Data Space [https://tds.okfn.gr/dataset/209]  
**Format:** Excel (.xlsx)  
**Key Fields:** Municipal_Community, Population  

---

## Dataset 3: Extended Population Dataset (Negotiated Access)
**Title:** Extended Resident Population Dataset – Thessaloniki Metropolitan Area (2011)  
**Description:** Extended demographic dataset provided after negotiation between the data provider (ELSTAT) and the researcher. It features higher spatial resolution at the sub-municipal level, enabling accurate mapping of population density and exposure. Access was granted under a graded access policy ensuring controlled reuse and citation obligations.  
**Source:** Internal Data Provision – Negotiated Access (MDAT)  
**Format:** Excel (.xlsx)  
**Key Fields:** Subunit, Population, Geographic_Code  

---

## Dataset 4: Derived Air Quality and Per-Capita Indicators (2010–2013)
**Title:** Derived Air Quality and Per-Capita Exposure Indicators (2010–2013)  
**Description:** Resulting dataset generated through the integration of air-quality measurements and extended population data. Includes computed pollutant means (2010–2013), WHO/EU compliance checks, and per-capita exposure metrics expressed as the Air Pollution Index per Capita (API_pc). The file represents the analytical output of the Thessaloniki Air Quality Workflow.  
**Source:** Local Analysis Script (Thessaloniki_AirQuality_Workflow.py)  
**Format:** Excel (.xlsx)  
**Key Fields:** Pollutant, Mean_2010_2013, Population, Pollution_per_Capita, Compliance_Status  

---

**Note:**  
All datasets comply with the **Data Privacy Vocabulary (DPV 2.2)** and **MDAT domain ontology**.  
Dataset 3 is categorized as *restricted access*, while Dataset 4 represents *derived analytical data*.
