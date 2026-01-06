## 1. Introduction

This document describes the research protocol for an indoor air quality study in sport facilities and residential environments. This protocol documents the study procedures based on the dataset structure and metadata.

## 2. Study Overview

The goal of the study was to track indoor air quality in various settings, with an emphasis on sports facilities like climbing halls and gyms. In order to determine how air quality indicators relate to occupancy patterns and activity intensity, the study integrated environmental sensor readings with subjective well-being assessments and cognitive performance tests.

## 3. Participants

Identified by participant IDs ranging from id088 to id108, the study comprised 22 participants. Data from each participant's home and place of employment (a sports facility) was gathered so that various indoor settings could be compared. Approximately 17 days of continuous monitoring were covered during the study period, which ran from June 29, 2025 to July 15, 2025.

## 4. Sensor Setup

### 4.1 AirControl Sensors

For each participant, fixed environmental sensors were placed in two different settings: their homes and workplaces (sports facilities). Three important air quality measures were continuously monitored by these sensors, which were positioned at fixed points across each location:

- **CO₂ concentration** measured in parts per million (ppm)
- **Temperature** measured in degrees Celsius (°C)
- **Relative humidity** measured as a percentage (%)

The location type and participant ID are used to organize the data files, and the file paths show whether the measurements were taken at home (named "House" or "Hause") or at work (labeled "Arbeit" in German, meaning job). Timestamped measurements are included in every sensor file; the timestamps are represented as date (DD/MM/YYYY) and time (HH:mm:ss), indicating continuous or high-frequency data logging during the study period.

### 4.2 AtmoTube Sensors

Mobile air quality measurements were gathered using portable AtmoTube sensors in addition to fixed sensors. Participants carried these portable gadgets, which enabled measurements in a variety of settings. A wider variety of environmental factors were recorded by the AtmoTube sensors:

- CO₂ concentration (ppm)
- Temperature (°C)
- Humidity (%)
- Volatile Organic Compounds (VOC) in ppm
- Air Quality Score (AQS)
- Particulate matter measurements: PM1, PM2.5, and PM10 (μg/m³)
- Atmospheric pressure (hPa)

Because these sensors were portable, they complemented the stationary AirControl sensors by providing information about changes in air quality as participants went through various areas.

## 5. Data Collection Procedures

### 5.1 Sensor Measurements

- **AirControl Sensors**: Continuous measurements logged with timestamps
  - Timestamp format: Date (DD/MM/YYYY) and Time (HH:mm:ss)
  - Measurement intervals: Appears to be continuous or high-frequency sampling
- **AtmoTube Sensors**: Measurements collected at specific dates
  - Multiple measurement sessions per participant
  - Date-based file naming convention

### 5.2 Survey Data Collection

Daily survey responses were collected from participants throughout the study period, resulting in 713 total survey entries. Each survey captured subjective assessments across five dimensions using Likert scales (1-7):

- **Stress level**: Participants' self-reported stress
- **Tiredness**: Level of fatigue or tiredness
- **Productivity**: Perceived productivity level
- **Thermal comfort**: How warm participants felt
- **Mental demand**: Cognitive load or mental effort required

These surveys were designed to capture participants' subjective experiences in relation to the environmental conditions being measured by the sensors.

### 5.3 Cognitive Performance Tests
Two types of cognitive performance assessments were integrated into the study:

- **Stroop Test**: Approximately 60% of the survey sessions were covered by the 429 Stroop tests that were given. Reaction time activities that recorded both congruent and incongruent answer durations were used in this test to assess cognitive ability. Accuracy, average reaction times for congruent and incongruent trials, and the Stroop effect (the difference between incongruent and congruent reaction times) were among the metrics offered by the test.

- **Creative Fluency Test**: In order to complete creative fluency exams, participants had to come up with original answers to word prompts. These assessments, which were administered to each participant several times using various word prompts, assessed their capacity for creative thought.

## 6. Data Organization

The dataset is organized hierarchically by participant ID, with each participant having a dedicated folder containing:

- AirControl sensor data organized by location type (work/home)
- AtmoTube sensor data files
- Survey responses (integrated into a unified survey file)
- Cognitive test results (Stroop and Creative tests)

This organization structure suggests a longitudinal design where multiple data streams were collected simultaneously from each participant across the study period.

## 7. Quality Assurance

While specific calibration procedures for the sensors are not detailed in the dataset, several indicators suggest that data quality measures were implemented:

1. **Measurement ranges**: The data values fall within physically plausible ranges for indoor environments:
   - CO₂ levels appropriate for indoor settings
   - Temperature and humidity values consistent with typical indoor conditions
   - Particulate matter measurements within expected ranges
2. **Data consistency**: Timestamp continuity and consistent file structures across participants indicate systematic data collection procedures.
3. **Temporal coverage**: The study period shows consistent data collection across the entire timeframe, suggesting reliable sensor operation and participant engagement.

During the analysis phase, additional quality assurance measures were applied, including outlier removal based on physical plausibility (CO₂: 300-5000 ppm, Temperature: 10-40°C, Humidity: 10-90%) and validation of timestamps and data formats.

## 8. Spatial Resolution

The study captured air quality data at two distinct spatial scales:  
1. **Fixed locations**: AirControl sensors provided continuous monitoring at specific fixed points within work (sport facilities) and home environments.  
2. **Mobile measurements**: AtmoTube sensors captured air quality variations as participants moved through different spaces, providing complementary spatial coverage.  

## 9. Ethical Considerations

Participants were only identifiable by participant IDs (id088 through id108) in the anonymised dataset. The data files contained no personally identifiable information, protecting participant privacy while preserving the capacity to connect several data streams from the same person.

## 10. Limitations and Notes

Certain aspects of the initial study processes might not be fully captured because this approach relies on inference from the dataset structure. The original data collecting would need to be consulted for specific details regarding sensor calibration techniques, precise measurement frequencies, exact sensor placement within locations, and comprehensive participant recruitment methods. Nonetheless, the file organization and dataset structure offer enough details to comprehend the general study design and data gathering methodology.

---


**Document prepared by**: MD Khasrur Rahman (12306556)  
**Date**: January 2026  
**Project**: Indoor Air Quality in Sport Facilities  
**Main Supervisor**: Assistant Professor Milica Vujovic, PhD  
**Co-Supervisor**: Senior Scientist Dr. Florina Piroi  