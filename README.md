# Credit Risk Analyst Dashboard

Analyze loan portfolio risk, compute Expected Credit Loss (ECL) by segment, and turn insights into clear policy actions.

This is my **Credit Risk Analyst Dashboard project for loan portfolio monitoring and decisioning**.

Live demo: [Credit Risk Analyst Dashboard](https://creditriskchat-uyxc8s5mmywyvcjmjwj3ne.streamlit.app/)

---

## 1. Overview

The app is built for risk teams who want a simple interface to:

- Upload loan-level data  
- Segment customers (for example by loan intent, education, home ownership, etc)  
- Compute ECL at segment level using PD, LGD and EAD  
- Visualize which segments drive the highest loss  
- Get AI generated recommendations  
- Let the CRO record final policy actions and track all submissions

All flows are implemented in a single Streamlit dashboard with role based access.

---

## 2. Key Features

### Authentication and Roles

- Login screen with role based access.
- Demo accounts:
  - `analyst / analyst123`
  - `cro / cro123`
- Role behavior:
  - **Analyst** – can upload datasets and run ECL for a single segment configuration.
  - **CRO** – can run ECL for multiple segments, view history, and record policy actions.

### Upload Loan Dataset

1. Navigate to **Upload Loan Dataset** after login.
2. Upload a CSV (e.g., `loan_data.csv`).
3. Preview the data before analysis.

### ECL Analysis Setup

- Choose columns to segment by (e.g., `loan_intent`, `person_home_ownership`).
- Click **Calculate ECL**.
- The app computes:
  - PD (Probability of Default)
  - LGD (Loss Given Default)
  - EAD (Exposure at Default)
  - ECL (Expected Credit Loss)

Formula used: **ECL = PD × LGD × EAD**

### ECL Curve Visualization

- View ECL across segments in a clear interactive chart.
- Identify high-risk loan segments.

### AI-Powered Recommendations

- Select a segment and click **Generate Recommendation**.
- The AI model suggests credit policy actions based on segment risk metrics.

### CRO Policy Actions & Submission History

- **CRO Policy Actions** – record actions per segment.
- **Submission History** – view all ECL analyses and policy decisions with timestamps and users.

---

## 3. Tech Stack

- **Framework:** Streamlit  
- **Language:** Python  
- **Libraries:** Pandas, NumPy, Plotly/Matplotlib  
- **Auth & Storage:** In-app credentials and data persistence  

---

## 4. Running the App Locally

```bash
# Clone repository
git clone <repo-url>
cd credit-risk-analyst-dashboard

# Create environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

---

## 5. Dataset Requirements

Include fields such as:

| Column | Description |
|---------|--------------|
| person_age | Age of applicant |
| person_gender | Gender |
| person_education | Education level |
| person_income | Annual income |
| person_home_ownership | RENT/OWN/MORTGAGE |
| loan_amnt | Loan amount |
| loan_intent | Purpose of loan |
| loan_int_rate | Interest rate |
| cb_person_cred_hist_length | Credit history length |

---

## 6. Use Cases

- Compare credit risk across loan intents and demographics.  
- Identify high-risk customer segments.  
- Generate explainable AI recommendations.  
- Record CRO decisions for audit and compliance.

---

## 7. Future Enhancements

- Integrate with production databases.  
- Add granular PD/LGD estimation models.  
- Enable export to PDF and PowerPoint.  
- Support real-time analytics for credit monitoring.

---

## 8. Screenshots

All screenshots of the working app are included above for reference – from login → upload → ECL analysis → AI recommendations → CRO actions.

---

**Author:** md arbab
**Institution:** Birla Institute of Technology, Mesra  
**Project Type:** Credit Risk Analysis (Loan Portfolio Monitoring & Decisioning)
