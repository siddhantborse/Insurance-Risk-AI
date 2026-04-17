# Surprise Medical Bill Risk Predictor - 15 Minute Presentation

## 📋 PRESENTATION FLOW (15 minutes)

### **SLIDE 1: Title Slide (0:00 - 0:30)**
- Project Title: "Surprise Medical Bill Risk Predictor"
- Team Members
- Institution: SDSU Big Data Analytics Capstone
- Date

---

### **SLIDE 2: Problem Statement (0:30 - 1:30)**
**"The Crisis"**

🔴 **Key Facts:**
- **$17 BILLION/year** in surprise medical bills in the US
- 43% of Americans struggle to pay medical bills
- Surprise bills average **$800-3,000** per incident

**Why it happens:**
1. Out-of-network specialists involved in care
2. Hidden ancillary services (radiology, anesthesia, pathology)
3. Large gaps between billed charges and insurance payments
4. Patients have ZERO visibility before receiving care

**Current state:**
- Patients discover bills AFTER care is delivered
- No decision-support tools exist
- Healthcare providers have information asymmetry

---

### **SLIDE 3: Solution Overview (1:30 - 2:30)**
**"Our Approach"**

🎯 **What We Built:**
A **predictive ML system** that scores surprise billing risk **BEFORE** services are delivered

**The Pipeline:**
```
Patient/Provider Input
    ↓
Feature Engineering (40+ indicators)
    ↓
ML Models (Classification + Regression)
    ↓
Risk Score + Financial Exposure + Source Identification
    ↓
Actionable Recommendations
```

**Key Innovation:**
- Predicts risk (not just reactive analysis)
- Works on publicly available CMS data
- Provides explainable predictions
- Runs on commodity hardware

---

### **SLIDE 4: Data & Feature Engineering (2:30 - 4:00)**
**"Turning Raw Data into Intelligence"**

**Data Source:**
- CMS Public Hospital Charge Data
- 100,000+ provider-service combinations
- States: All US states (nationwide coverage)

**Key Features Engineered:**

1. **Financial Features:**
   - Charge Ratio = Billed Amount / Medicare Payment
   - Payment Gap = Billed Amount - Medicare Payment
   - Provider Risk Index (historical overcharging)
   - State Risk Index (geographic patterns)

2. **Service Features:**
   - ER/Emergency flag
   - Imaging/Radiology flag
   - Surgical procedure flag
   - Anesthesia involvement flag
   - Pathology flag
   - High-complexity DRG flag

3. **Aggregated Features:**
   - Provider-level charge patterns
   - State-level benchmarks
   - Service-type risk weights

**Total Features: 40+**

---

### **SLIDE 5: Machine Learning Models (4:00 - 5:30)**
**"Three Specialized Models"**

**Model 1: Risk Classification**
- **Algorithm:** Random Forest Classifier
- **Target:** Surprise bill probability (0-1)
- **Performance:** AUC = 0.8X (insert real value)
- **Output:** Risk score, risk band (Low/Moderate/High)

**Model 2: Exposure Regression**
- **Algorithm:** Random Forest Regressor
- **Target:** Expected dollar amount of surprise bill
- **Performance:** MAE = $XXX (insert real value)
- **Output:** Predicted extra cost

**Model 3: Multi-Label Source Prediction**
- **Algorithm:** One-vs-Rest Logistic Regression
- **Target:** Likely billing sources (Anesthesia, Radiology, Pathology)
- **Output:** Probability each source will cause surprise bill

---

### **SLIDE 6: Model Results & Validation (5:30 - 7:00)**
**"Does It Work?"**

**Classification Performance:**
```
ROC-AUC: 0.8X
Precision: X.XX
Recall: X.XX
F1-Score: X.XX
```

**Regression Performance:**
```
MAE: $XXX
RMSE: $XXX
R² Score: X.XX
```

**Real-World Example:**
Show a sample case prediction:
- Patient scenario (service type, provider, state)
- Model outputs (risk %, exposure $, sources)
- Comparison to actual data statistics

---

### **SLIDE 7: Live Dashboard Demo (7:00 - 9:00)**
**"Interactive Risk Calculator"**

📊 **Demo:**
1. Walk through the Streamlit dashboard
2. Show "Risk Calculator" page
3. Input example patient scenario
4. Run prediction live
5. Show breakdown of risk factors
6. Display recommendations

**Features Shown:**
- Risk scoring
- Financial exposure estimation
- Service risk breakdown
- Patient action items checklist

---

### **SLIDE 8: SWOT Analysis (9:00 - 10:30)**
**"Strategic Assessment"**

**STRENGTHS:** 4-5 bullet points
- Real $17B problem
- Predictive (not reactive)
- Data-driven & interpretable
- Scalable across geographies
- Works on normal laptops

**WEAKNESSES:** 3-4 bullet points
- Proxy labels (no ground truth)
- CMS data lag (6-12 months)
- Medicare data only
- Depends on provider data quality

**OPPORTUNITIES:** 4-5 bullet points
- Insurance partnerships (UnitedHealth, Aetna)
- Hospital pre-admission screening
- Patient mobile app
- International expansion
- Regulatory compliance tool

**THREATS:** 3-4 bullet points
- Provider resistance
- Privacy/HIPAA compliance
- Competition from health-tech giants
- Regulatory changes

---

### **SLIDE 9: Business Impact & Use Cases (10:30 - 11:30)**
**"Who Uses This?"**

**1. Patients:**
- Get risk assessment before scheduling care
- Know likely sources of surprise bills
- Get actionable recommendations

**2. Insurance Companies:**
- Flag high-risk provider relationships
- Prioritize network adequacy reviews
- Reduce surprise bill claims

**3. Hospitals:**
- Identify billing compliance gaps
- Improve transparency
- Reduce patient complaints

**4. Healthcare Regulators:**
- Monitor compliance with No Surprises Act
- Identify repeat offenders
- Enforce regulatory requirements

---

### **SLIDE 10: Deployment & Next Steps (11:30 - 13:00)**
**"From Notebook to Product"**

**Current State:**
✅ Data pipeline (notebooks 1-4)
✅ ML models trained & saved
✅ Interactive Streamlit dashboard

**Next Steps (Phase 1):**
- Partner with 3-5 hospitals for validation
- Validate predictions against actual surprise bills
- Refine model with real ground truth

**MVP Phase (Phase 2):**
- Build patient-facing mobile app
- Integrate with insurance platforms
- Launch beta with 50+ providers

**Scale Phase (Phase 3):**
- Fundraising & Series A
- Expand internationally
- Build enterprise platform

---

### **SLIDE 11: Technical Stack & Innovation (13:00 - 14:00)**
**"How We Built It"**

**Technology:**
- **Data:** Python, Pandas, Parquet
- **ML:** Scikit-learn (Random Forest, Logistic Regression)
- **Features:** 40+ engineered indicators
- **Dashboard:** Streamlit + Plotly
- **Models:** Saved as joblib artifacts

**Innovation:**
- Proxy label creation (simulating ground truth)
- Blended financial features (inpatient + outpatient)
- Service-specific risk weights
- Multi-model architecture

**Scalability:**
- No GPU required (runs on laptops)
- Modular design (easy to add data/models)
- Can score new cases in <100ms

---

### **SLIDE 12: Conclusion & Call to Action (14:00 - 15:00)**
**"Impact & Vision"**

**Key Takeaway:**
Surprise medical billing is a solvable problem. Data + ML + good design can help patients make informed healthcare decisions.

**Vision:**
"Empower 10M+ patients with transparency before healthcare decisions"

**Call to Action:**
- Interest in piloting at your hospital?
- Questions about the approach?
- Interested in the team?

---

## 📊 VISUAL AIDS CHECKLIST

**Create these visualizations:**
- [ ] Problem statement infographic ($17B, statistics)
- [ ] Data flow diagram (notebook 1 → 4)
- [ ] Feature engineering examples (before/after)
- [ ] Model architecture diagram
- [ ] Sample prediction breakdown
- [ ] SWOT quadrant diagram
- [ ] Use case icons (Patient, Insurer, Hospital, Regulator)
- [ ] Deployment roadmap timeline

---

## 🎤 DELIVERY TIPS

1. **Practice Timing:** Rehearse to hit exactly 15 minutes
2. **Live Demo:** Have dashboard loaded and ready
3. **Backup:** Screenshot of dashboard in case connection fails
4. **Questions:** Prepare answers for:
   - "How is this different from X competitor?"
   - "What about HIPAA/privacy?"
   - "How do you validate predictions?"
   - "What's the business model?"
5. **Energy:** Start strong, maintain pace, end with inspiration

---

## 📁 PRESENTATION FILES NEEDED

```
📦 Capstone_Presentation/
├── Slides.pptx (or Google Slides link)
├── Dashboard_Screenshots.pdf (backup)
├── SWOT_Diagram.png
├── Data_Flow_Diagram.png
├── Feature_Engineering_Example.pdf
├── Model_Results_Table.png
└── Delivery_Notes.docx
```

---

## ⏱️ TIME ALLOCATION

| Section | Duration | Notes |
|---------|----------|-------|
| Problem Statement | 1:00 | Set urgency & need |
| Solution Overview | 1:00 | Quick technical brief |
| Data & Features | 1:30 | Show engineering depth |
| ML Models | 1:30 | Technical credibility |
| Results | 1:30 | Prove it works |
| Dashboard Demo | 2:00 | **LIVE DEMO** (most engaging) |
| SWOT Analysis | 1:30 | Show strategic thinking |
| Business Impact | 1:00 | Real-world relevance |
| Deployment | 1:30 | Future vision |
| Conclusion | 1:00 | Memorable ending |
| **TOTAL** | **15:00** | |

