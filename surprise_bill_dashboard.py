import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Surprise Medical Bill Risk Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .risk-high { color: #d32f2f; font-weight: bold; }
    .risk-medium { color: #f57c00; font-weight: bold; }
    .risk-low { color: #388e3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD ARTIFACTS
# ============================================================================
@st.cache_resource
def load_models():
    try:
        clf = joblib.load("artifacts/risk_classifier.joblib")
        reg = joblib.load("artifacts/exposure_regressor.joblib")
        src = joblib.load("artifacts/source_predictor.joblib")
        with open("artifacts/model_metrics.json") as f:
            metrics = json.load(f)
        return clf, reg, src, metrics
    except:
        st.error("❌ Models not found. Please ensure artifacts are in 'artifacts/' folder")
        return None, None, None, None

@st.cache_data
def load_data():
    try:
        df = pd.read_parquet("data/model_features.parquet")
        return df
    except:
        st.warning("⚠️ Data not found. Some features disabled.")
        return None

clf, reg, src, metrics = load_models()
df = load_data()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.title("🏥 Surprise Bill Predictor")
page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "🔬 Risk Calculator",
    "📊 Analytics",
    "⚙️ Model Performance",
    "📋 SWOT Analysis"
])

# ============================================================================
# PAGE 1: HOME
# ============================================================================
if page == "🏠 Home":
    st.title("Surprise Medical Bill Risk Predictor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Problem Statement
        Patients receive **$17 billion/year in surprise medical bills** due to:
        - Out-of-network providers
        - Hidden service costs
        - Payment gaps between billed and insured amounts
        
        **Our Solution:** Predict this risk BEFORE care is delivered.
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 How It Works
        1. **Analyze** provider pricing patterns
        2. **Engineer** risk features (charge ratios, payment gaps)
        3. **Predict** surprise billing probability
        4. **Estimate** financial exposure
        5. **Identify** likely risk sources
        """)
    
    st.divider()
    
    # Key metrics
    if metrics:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Classification AUC", f"{metrics['classification_auc']:.3f}")
        with col2:
            st.metric("Regression MAE ($)", f"${metrics['regression_mae']:.0f}")
        with col3:
            st.metric("RMSE ($)", f"${metrics['regression_rmse']:.0f}")
        with col4:
            st.metric("R² Score", f"{metrics['regression_r2']:.3f}")
    
    st.divider()
    
    # Dataset overview
    if df is not None:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"📊 Total Records: {len(df):,}")
        with col2:
            st.info(f"🏥 Unique Providers: {df['provider_id'].nunique():,}")
        with col3:
            st.info(f"🗺️ States Covered: {df['provider_state'].nunique()}")
    
    st.divider()
    
    # Technology stack
    st.markdown("""
    ### 💻 Technology Stack
    - **Data**: CMS Public Healthcare Data
    - **ML**: Scikit-learn (Random Forest, Logistic Regression)
    - **Features**: 40+ engineered financial & service indicators
    - **Models**: Classification + Regression + Multi-label
    - **Dashboard**: Streamlit + Plotly
    """)

# ============================================================================
# PAGE 2: RISK CALCULATOR
# ============================================================================
elif page == "🔬 Risk Calculator":
    st.title("Risk Calculator - Score a New Case")
    
    st.markdown("""
    Enter patient/provider details below to get a personalized risk assessment.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_covered = st.number_input("Avg Covered Charges ($)", value=42000, min_value=0, step=1000)
        avg_payments = st.number_input("Avg Total Payments ($)", value=16500, min_value=0, step=1000)
    
    with col2:
        billed_amount = st.number_input("Billed Amount ($)", value=6800, min_value=0, step=100)
        medicare_payment = st.number_input("Medicare Payment ($)", value=2400, min_value=0, step=100)
    
    with col3:
        state = st.selectbox("Provider State", ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI"] if df is not None else ["CA"])
        service_type = st.selectbox("Service Type", [
            "outpatient surgery",
            "emergency department",
            "imaging",
            "inpatient surgery",
            "same-day procedure"
        ])
    
    # Service flags
    col1, col2, col3, col4 = st.columns(4)
    is_er = col1.checkbox("Emergency (ER)?", value=False)
    is_imaging = col2.checkbox("Includes Imaging?", value=True)
    is_surgery = col3.checkbox("Surgical Procedure?", value=True)
    is_outpatient = col4.checkbox("Outpatient?", value=True)
    
    if st.button("🔍 Calculate Risk", use_container_width=True):
        if clf is not None and reg is not None and src is not None:
            # Prepare scenario
            eps = 1e-6
            scenario = {
                "average_covered_charges": avg_covered,
                "average_total_payments": avg_payments,
                "Billed amount": billed_amount,
                "Medicare payment": medicare_payment,
                "provider_state": state,
                "service_type": service_type,
                "drg_text": f"{service_type} with review",
                "is_er": int(is_er),
                "is_imaging": int(is_imaging),
                "is_outpatient": int(is_outpatient),
                "is_surgery": int(is_surgery),
                "high_complexity_drg": int(is_surgery),
            }
            
            # Compute derived features
            charge_ratio_inp = avg_covered / (avg_payments + eps)
            payment_gap_inp = avg_covered - avg_payments
            charge_ratio_out = billed_amount / (medicare_payment + eps)
            payment_gap_out = billed_amount - medicare_payment
            
            scenario.update({
                "charge_ratio_inpatient": charge_ratio_inp,
                "payment_gap_inpatient": payment_gap_inp,
                "charge_ratio_outpatient": charge_ratio_out,
                "payment_gap_outpatient": payment_gap_out,
                "blended_charge_ratio": charge_ratio_out if charge_ratio_out > 0 else charge_ratio_inp,
                "blended_payment_gap": payment_gap_out if payment_gap_out > 0 else payment_gap_inp,
                "log_avg_covered": np.log1p(avg_covered),
                "log_avg_payments": np.log1p(avg_payments),
                "log_billed_amount": np.log1p(billed_amount),
                "log_medicare_payment": np.log1p(medicare_payment),
                "log_blended_gap": np.log1p(max(payment_gap_out if payment_gap_out > 0 else payment_gap_inp, 0)),
            })
            
            # Add state defaults if available
            if df is not None:
                state_data = df[df["provider_state"] == state][
                    ["provider_avg_gap", "provider_gap_std", "provider_avg_ratio", "provider_record_count",
                     "state_avg_gap", "state_avg_ratio", "state_median_payment", "state_record_count",
                     "provider_risk_index", "state_risk_index"]
                ]
                if not state_data.empty:
                    state_defaults = state_data.median().to_dict()
                    scenario.update(state_defaults)
                else:
                    # Use global defaults
                    scenario.update({
                        "provider_avg_gap": df["provider_avg_gap"].median() if df is not None else 5000,
                        "provider_gap_std": df["provider_gap_std"].median() if df is not None else 2000,
                        "provider_avg_ratio": df["provider_avg_ratio"].median() if df is not None else 1.5,
                        "provider_record_count": 50,
                        "state_avg_gap": df["state_avg_gap"].median() if df is not None else 4000,
                        "state_avg_ratio": df["state_avg_ratio"].median() if df is not None else 1.4,
                        "state_median_payment": df["state_median_payment"].median() if df is not None else 8000,
                        "state_record_count": 1000,
                        "provider_risk_index": 0.4,
                        "state_risk_index": 0.5,
                    })
            
            scenario["service_risk_weight"] = (
                0.35 * scenario["is_er"] +
                0.25 * scenario["is_surgery"] +
                0.15 * scenario["is_imaging"] +
                0.15 * scenario["high_complexity_drg"]
            )
            
            # Score
            scenario_df = pd.DataFrame([scenario])
            
            # Get model features
            model_features = [
                "average_covered_charges", "average_total_payments", "Billed amount", "Medicare payment",
                "charge_ratio_inpatient", "payment_gap_inpatient", "charge_ratio_outpatient", "payment_gap_outpatient",
                "blended_charge_ratio", "blended_payment_gap", "log_avg_covered", "log_avg_payments",
                "log_billed_amount", "log_medicare_payment", "log_blended_gap",
                "is_er", "is_imaging", "is_outpatient", "is_surgery", "high_complexity_drg",
                "provider_avg_gap", "provider_gap_std", "provider_avg_ratio", "provider_record_count",
                "state_avg_gap", "state_avg_ratio", "state_median_payment", "state_record_count",
                "provider_risk_index", "state_risk_index", "service_risk_weight",
                "provider_state", "service_type", "drg_text"
            ]
            
            score_X = scenario_df[model_features]
            risk_prob = float(clf.predict_proba(score_X)[:, 1][0])
            exposure = float(reg.predict(score_X)[0])
            
            # Display results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if risk_prob >= 0.67:
                    risk_color = "🔴"
                    risk_band = "HIGH RISK"
                elif risk_prob >= 0.34:
                    risk_color = "🟡"
                    risk_band = "MODERATE RISK"
                else:
                    risk_color = "🟢"
                    risk_band = "LOW RISK"
                
                st.markdown(f"""
                ### {risk_color} Risk Assessment
                **{risk_band}**
                
                Probability: **{risk_prob:.1%}**
                """)
            
            with col2:
                st.markdown(f"""
                ### 💰 Financial Exposure
                Estimated Extra Bill:
                
                **${max(exposure, 0):,.2f}**
                """)
            
            with col3:
                st.markdown(f"""
                ### 📊 Key Metrics
                - Charge Ratio: **{scenario['blended_charge_ratio']:.2f}x**
                - Payment Gap: **${scenario['blended_payment_gap']:,.0f}**
                - Provider Risk Index: **{scenario['provider_risk_index']:.2f}**
                """)
            
            st.divider()
            
            # Risk breakdown
            st.markdown("### 🎯 Risk Breakdown")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Financial Risk Factors:**
                - Charge Ratio vs Market: {'🔴 HIGH' if scenario['blended_charge_ratio'] > 1.5 else '🟢 NORMAL'}
                - Payment Gap: ${scenario['blended_payment_gap']:,.0f}
                """)
            
            with col2:
                st.markdown(f"""
                **Service Risk Factors:**
                - Emergency Care: {'Yes 🔴' if is_er else 'No 🟢'}
                - Surgery: {'Yes 🔴' if is_surgery else 'No 🟢'}
                - Imaging: {'Yes ⚠️' if is_imaging else 'No 🟢'}
                """)
            
            st.divider()
            
            # Recommendations
            st.markdown("### 📋 Patient Action Items")
            
            recommendations = [
                "✅ Ask whether any clinicians will bill separately from the facility.",
                "✅ Request a written estimate including all facility and professional components.",
            ]
            
            if scenario.get("provider_risk_index", 0) >= 0.6:
                recommendations.append("⚠️ Call your insurance company BEFORE care to verify network status.")
            
            if is_imaging:
                recommendations.append("📸 Confirm whether imaging will be interpreted by an external radiology group.")
            
            if is_surgery:
                recommendations.append("🏥 Ask which anesthesia group will be used and verify network status.")
            
            for rec in recommendations:
                st.markdown(rec)
        else:
            st.error("⚠️ Models not loaded. Please check artifacts folder.")

# ============================================================================
# PAGE 3: ANALYTICS
# ============================================================================
elif page == "📊 Analytics":
    st.title("Healthcare Analytics Dashboard")
    
    if df is not None:
        # State-level analytics
        st.markdown("### 🗺️ Risk by State")
        
        state_agg = df.groupby("provider_state").agg({
            "proxy_surprise_bill_label": "mean",
            "proxy_exposure_amount": "mean",
            "blended_payment_gap": "mean",
            "provider_id": "count"
        }).reset_index()
        state_agg.columns = ["State", "Avg Risk %", "Avg Exposure", "Avg Gap", "Records"]
        state_agg = state_agg.sort_values("Avg Risk %", ascending=False).head(15)
        
        fig_state = px.bar(
            state_agg.sort_values("Avg Risk %"),
            x="Avg Risk %",
            y="State",
            orientation="h",
            title="Top States by Surprise Bill Risk",
            color="Avg Risk %",
            color_continuous_scale="RdYlGn_r"
        )
        st.plotly_chart(fig_state, use_container_width=True)
        
        st.dataframe(state_agg, use_container_width=True)
        
        st.divider()
        
        # Service type analytics
        st.markdown("### 🏥 Risk by Service Type")
        
        service_agg = df.groupby("service_type").agg({
            "proxy_surprise_bill_label": "mean",
            "proxy_exposure_amount": "mean",
            "provider_id": "count"
        }).reset_index()
        service_agg.columns = ["Service", "Risk %", "Avg Exposure", "Count"]
        service_agg = service_agg[service_agg["Count"] > 10].sort_values("Risk %", ascending=False)
        
        fig_service = px.bar(
            service_agg,
            x="Service",
            y="Risk %",
            color="Risk %",
            title="Risk Profile by Service Type",
            color_continuous_scale="RdYlGn_r"
        )
        st.plotly_chart(fig_service, use_container_width=True)
        
        st.divider()
        
        # Charge ratio distribution
        st.markdown("### 💹 Charge Ratio Distribution")
        
        fig_ratio = px.histogram(
            df,
            x="blended_charge_ratio",
            nbins=50,
            title="Billed vs Insured Amount Ratio",
            labels={"blended_charge_ratio": "Charge Ratio"},
            color_discrete_sequence=["#1f77b4"]
        )
        fig_ratio.add_vline(x=1.5, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
        st.plotly_chart(fig_ratio, use_container_width=True)
        
        st.divider()
        
        # Top risky providers
        st.markdown("### ⚠️ Top 20 Riskiest Providers")
        
        provider_risk = df.groupby(["provider_id", "provider_name", "provider_state"]).agg({
            "proxy_surprise_bill_label": "mean",
            "proxy_exposure_amount": "mean",
            "blended_payment_gap": "mean",
            "provider_id": "count"
        }).reset_index(drop=False)
        provider_risk.columns = ["Provider ID", "Provider Name", "State", "Risk %", "Avg Exposure", "Avg Gap", "Records"]
        provider_risk = provider_risk[provider_risk["Records"] > 5].sort_values("Risk %", ascending=False).head(20)
        
        st.dataframe(provider_risk, use_container_width=True, hide_index=True)
    
    else:
        st.warning("📊 Data not available for analytics.")

# ============================================================================
# PAGE 4: MODEL PERFORMANCE
# ============================================================================
elif page == "⚙️ Model Performance":
    st.title("Machine Learning Model Performance")
    
    if metrics:
        st.markdown("""
        ## Model Architecture
        
        **3 Specialized Models:**
        1. **Risk Classifier** - Predicts surprise billing probability
        2. **Exposure Regressor** - Estimates financial exposure amount
        3. **Source Predictor** - Identifies billing sources (multi-label)
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Classification Model")
            st.info(f"""
            **Algorithm:** Random Forest Classifier
            
            **Performance:**
            - ROC-AUC: **{metrics['classification_auc']:.3f}**
            - Features: 40+ engineered indicators
            - Training samples: ~80,000+
            """)
        
        with col2:
            st.markdown("### Regression Model")
            st.info(f"""
            **Algorithm:** Random Forest Regressor
            
            **Performance:**
            - MAE: **${metrics['regression_mae']:.0f}**
            - RMSE: **${metrics['regression_rmse']:.0f}**
            - R² Score: **{metrics['regression_r2']:.3f}**
            """)
        
        st.divider()
        
        st.markdown("### 📊 Feature Importance")
        
        st.markdown("""
        Top features driving risk predictions:
        1. **Charge Ratio** - Billed vs Medicare payment ratio
        2. **Payment Gap** - Dollar difference between billed and insured
        3. **Provider Risk Index** - Historical overcharging patterns
        4. **Service Type Flags** - ER, Surgery, Imaging risk weights
        5. **State Risk Index** - Geographic risk aggregates
        """)
    
    else:
        st.error("Models not loaded")

# ============================================================================
# PAGE 5: SWOT ANALYSIS
# ============================================================================
elif page == "📋 SWOT Analysis":
    st.title("SWOT Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💪 STRENGTHS
        
        ✅ **Real Problem:** Addresses $17B/year surprise billing crisis
        
        ✅ **Predictive:** Prevents bills BEFORE they occur
        
        ✅ **Data-Driven:** Uses 40+ engineered financial indicators
        
        ✅ **Interpretable:** Clear feature importance & explainability
        
        ✅ **Scalable:** Works across providers and states
        
        ✅ **Lightweight:** Runs on normal laptops (no GPU)
        
        ✅ **Modular:** Classification + Regression + Multi-label
        """)
        
        st.markdown("""
        ### 🚀 OPPORTUNITIES
        
        🔗 **Insurance Integration:** Partner with UnitedHealth, Aetna, Cigna
        
        🏥 **Hospital Adoption:** Pre-admission screening tool
        
        📱 **Patient App:** Consumer-facing mobile application
        
        ⚖️ **Regulatory:** Compliance tool for healthcare systems
        
        🔄 **Real-time Data:** Claims processor partnerships
        
        🌍 **International:** Expand to other markets
        
        💼 **B2B2C:** White-label for health tech platforms
        """)
    
    with col2:
        st.markdown("""
        ### ⚠️ WEAKNESSES
        
        ❌ **Proxy Labels:** No actual ground truth surprises
        
        ❌ **Data Lag:** CMS data 6-12 months old
        
        ❌ **Limited Scope:** Medicare data only
        
        ❌ **Quality Dependent:** Relies on provider data accuracy
        
        ❌ **No Network Integration:** Doesn't use insurance networks
        
        ❌ **One-Model Approach:** Could ensemble multiple algorithms
        
        ❌ **Missing Context:** No clinical severity scores
        """)
        
        st.markdown("""
        ### 🛡️ THREATS
        
        🔴 **Provider Resistance:** Threatens provider revenue models
        
        🔐 **Privacy:** HIPAA compliance & data security costs
        
        📊 **Data Access:** Regulatory restrictions on CMS data
        
        ⚖️ **Regulatory:** Federal surprise billing law (No Surprises Act)
        
        🏢 **Competition:** Established health-tech giants (Optum, CVS Health)
        
        💰 **Reimbursement:** Changes to payment models
        
        🎯 **Adoption:** Provider & insurer resistance to new systems
        """)
    
    st.divider()
    
    st.markdown("""
    ## 🎯 Strategic Recommendations
    
    ### Phase 1: Validation (Q1-Q2)
    - Partner with 3-5 pilot hospitals
    - Validate predictions against actual surprise bills
    - Refine model with real ground truth data
    
    ### Phase 2: MVP (Q3-Q4)
    - Build patient-facing mobile app
    - Integrate with major insurance carriers
    - Launch beta program with 100+ providers
    
    ### Phase 3: Scale (Year 2)
    - Secure Series A funding
    - Expand to 50+ states & international markets
    - Build enterprise platform for health systems
    """)

st.sidebar.divider()
st.sidebar.markdown("""
---
**Surprise Medical Bill Risk Predictor**  
SDSU Big Data Analytics Capstone  
2024-2025

Built with: Python, Scikit-learn, Streamlit, Plotly
""")
