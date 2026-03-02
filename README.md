# Digital Marketing Performance AI (SQL + Tableau + AI Copilot)

A portfolio project that simulates **B2B digital marketing analytics** using **SQL + Tableau dashboards + an LLM-powered AI Copilot** to generate grounded insights and recommendations.

## 🔗 Live Dashboard (Tableau Public)
Interactive dashboard:
https://public.tableau.com/app/profile/bhaghirathi.kundu8438/viz/digital-marketing-performance-dashboard/MarketingPerformanceDashboard?publish=yes

---

## 📌 What this project demonstrates
- **Funnel performance** (Sessions → Signups) across channels
- **Channel analytics**: sessions, signups, conversion (signup rate), bounce rate
- **ROI / Efficiency quadrant** to identify “scale vs fix” channels
- **Tableau storytelling**: KPI tiles, heatmap, funnel view, scatter/quadrant
- **AI Copilot**: LLM-generated recommendations grounded in your dataset

---

## 📊 Dashboard Views (What to look for)
### 1) KPI Tiles
High-level metrics for the last 30 days:
- Total Sessions
- Total Signups
- Overall Conversion Rate (Signups / Sessions)
- Avg Bounce Rate

### 2) Channel Performance Heatmap
Quick comparison of channel performance across multiple metrics:
- Sessions (volume)
- Signups (outcome)
- Signup Rate (efficiency)
- Bounce Rate (traffic quality)

### 3) Funnel View by Channel
Sessions vs Signups per channel to visualize drop-off.

### 4) ROI / Efficiency Quadrant
Scatter plot segmented by median lines:
- High sessions + high signup rate → **Scale**
- High sessions + low signup rate → **Fix funnel**
- Low sessions + high signup rate → **Invest / test scaling**
- Low sessions + low signup rate → **Deprioritize**

---

## 🤖 AI Copilot (LLM Recommendations)
This repo includes an **AI Marketing Copilot** built in Streamlit that:
- Answers questions like: “What should we optimize next?”
- Surfaces underperforming channels with concrete fixes
- Produces weekly briefs & actionable recommendations
- Stays grounded in the data snapshot generated from the dataset

### Example prompts
- “Which channels should we scale and why?”
- “Which channels need conversion fixes? Suggest experiments.”
- “Summarize last 30 days and top 3 actions for next week.”

---

## 🧱 Tech Stack
- **Tableau Public** (dashboard + storytelling)
- **SQL** (analysis scripts / validation)
- **Python** (data loading & summarization)
- **Streamlit** (AI Copilot UI)
- **OpenAI API** (LLM reasoning & recommendations)

---

## 📁 Repository Structure
