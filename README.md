# EnrollmentForecasting
Forecasting Enrollment by state, using data to drive decision making on higher ed policy. Currently using AI to teach me professional level workflows and quality.

# Research Framework: State Undergraduate Enrollment Trends (2012-2022)

## Summary
This study examines undergraduate enrollment patterns across U.S. states from 2012-2022, investigating demographic, economic, and institutional factors that drive enrollment changes. The analysis aims to identify at-risk states, understand the public-private enrollment dynamic, and assess the predictability of future enrollment trends.

---

## Questions

### 1. Descriptive Analysis: Understanding Enrollment Patterns

**1.1: Temporal Trends**
*How has undergraduate enrollment changed across U.S. states from 2012-2022, and are these changes statistically significant?*

- **Sub-questions:**
  - What is the national enrollment trend when aggregating across all states?
  - Which states show statistically significant declining trends? (α = 0.05)
  - Which states show statistically significant growth trends?
  - What is the effect size of enrollment changes (Cohen's d)?
  - Are there inflection points where enrollment trends shifted direction?

- **Success Metrics:**
  - Identify states with |slope| > X and p < 0.05
  - Calculate year-over-year growth rates with 95% confidence intervals
  - Determine if majority of states are declining (binomial test)

- **Analysis Methods:**
  - Mann-Kendall trend test for each state
  - Linear regression with significance testing
  - Breakpoint/changepoint analysis for trend shifts
  - Effect size calculations (Cohen's d)

---

**1.2: Institutional Type Analysis**
*How do enrollment trends differ between public and private institutions, and is this difference statistically significant?*

- **Sub-questions:**
  - Is the public-to-private enrollment ratio changing over time?
  - Are public institutions declining faster/slower than private institutions?
  - What is the effect size of this difference?
  - Are there states where private institutions are growing while public decline (or vice versa)?

- **Success Metrics:**
  - Paired t-test comparing public vs private growth rates (p < 0.05)
  - Calculate weighted vs unweighted public-private ratios
  - Identify states with diverging public/private trends

- **Analysis Methods:**
  - Paired t-tests or Wilcoxon signed-rank tests
  - Time series analysis of public-private ratio
  - State-level comparison of institutional trajectories

---

**1.3: Geographic Patterns**
*Do enrollment trends cluster geographically, and what regional patterns emerge?*

- **Sub-questions:**
  - Are Northeastern states experiencing different trends than Southern/Western states?
  - Is there spatial autocorrelation in enrollment trends? (Do neighboring states behave similarly?)
  - Are urban vs rural states showing different patterns?
  - Which Census regions/divisions show the strongest declines?

- **Success Metrics:**
  - ANOVA comparing regions (p < 0.05)
  - Moran's I for spatial autocorrelation
  - Regional effect sizes

- **Analysis Methods:**
  - Regional grouping analysis (Census regions)
  - Spatial statistics (Moran's I, spatial lag models)
  - Choropleth mapping with statistical overlays

---

## Secondary Research Questions

### 2. Causal/Explanatory Analysis: Drivers of Enrollment Change

**2.1: Demographic Drivers**
*What demographic factors are associated with state-level enrollment changes?*

- **Variables to Acquire:**
  - High school graduation rates (by state, by year)
  - 18-24 year-old population (college-age cohort size)
  - Net migration of college-age population
  - Birth rates (lagged 18 years)
  - Racial/ethnic demographic composition changes
  - Urbanization rates

- **Hypotheses:**
  - H1: States with declining college-age populations show enrollment declines
  - H2: States with increasing high school graduation rates show enrollment increases
  - H3: Net out-migration of young adults correlates with enrollment decline

- **Analysis Methods:**
  - Correlation analysis (Pearson/Spearman)
  - Multiple regression: Enrollment ~ Demographics + Controls
  - Lagged correlation analysis (demographic changes precede enrollment)
  - Fixed-effects panel regression models

---

**2.2: Economic Drivers**
*How do economic conditions affect enrollment trends?*

- **Variables to Acquire:**
  - Median household income (state-level)
  - Unemployment rate (state-level, especially youth unemployment)
  - State GDP growth
  - Tuition costs (public and private, in-state and out-of-state)
  - State funding for higher education (appropriations per student)
  - Student debt levels
  - Financial aid availability

- **Hypotheses:**
  - H4: Higher tuition growth correlates with enrollment decline
  - H5: Lower unemployment correlates with enrollment decline (opportunity cost)
  - H6: Reduced state funding correlates with enrollment decline
  - H7: Economic recessions correlate with enrollment increases (countercyclical)

- **Analysis Methods:**
  - Time-lagged correlation (economic changes may precede enrollment by 1-2 years)
  - Multiple regression with economic controls
  - Difference-in-differences for policy changes (e.g., states that cut/increased funding)
  - Elasticity calculations (% enrollment change per % tuition change)

---

**2.3: Policy and Institutional Drivers**
*Do state policies and institutional characteristics influence enrollment?*

- **Variables to Acquire:**
  - Free community college policies (states with/without)
  - Promise program implementations
  - College readiness initiatives
  - Number of institutions per capita
  - Online program availability
  - Admission selectivity trends
  - Tenure-track faculty ratios

- **Hypotheses:**
  - H8: States implementing promise programs show enrollment increases
  - H9: States with more community colleges per capita show different trends
  - H10: Increased online program availability correlates with enrollment stability

- **Analysis Methods:**
  - Quasi-experimental designs (comparing states with/without policies)
  - Event study analysis (before/after policy implementation)
  - Synthetic control methods
  - Interrupted time series analysis

---

**2.4: COVID-19 Impact**
*Did the COVID-19 pandemic differentially affect enrollment across states?*

- **Sub-questions:**
  - Was there an abnormal enrollment decline in 2020-2021?
  - Did the decline vary by state characteristics (e.g., online infrastructure)?
  - Have enrollments recovered in 2022?
  - Did COVID accelerate pre-existing trends or create new ones?

- **Analysis Methods:**
  - Interrupted time series analysis (pre-COVID vs COVID vs post-COVID)
  - Difference-in-differences (comparing states with different COVID responses)
  - Counterfactual analysis (what would 2020-21 enrollment have been without COVID?)

---

### 3. Predictive Analysis: Forecasting Future Enrollment

**3.1: Time Series Forecasting**
*Can we accurately predict state-level enrollment for 2023-2025 using historical trends?*

- **Approach:**
  - Baseline: Naive forecasts (assume continuation of recent trend)
  - ARIMA models for each state
  - Exponential smoothing (Holt-Winters)
  - Prophet (Facebook's time series tool)
  - Ensemble methods

- **Success Metrics:**
  - RMSE, MAE, MAPE on test set (hold out 2021-2022 for validation)
  - Directional accuracy (% of states where trend direction is correct)
  - Confidence intervals for predictions

- **Limitations to Acknowledge:**
  - Limited time points (10-12 years)
  - Structural breaks (COVID) may reduce predictability
  - Predictions beyond 2-3 years increasingly uncertain

---

**3.2: Multivariate Predictive Modeling**
*Can demographic and economic indicators improve enrollment forecasts?*

- **Approach:**
  - Feature engineering from demographic/economic data
  - Multiple regression with lagged predictors
  - Random Forest / Gradient Boosting for non-linear relationships
  - Panel data models (fixed effects, random effects)
  - Cross-validation by state or time

- **Key Question:**
  - Which variables have the strongest predictive power?
  - Feature importance analysis
  - Marginal effects interpretation

- **Success Metrics:**
  - Compare R² and prediction error vs time-series-only models
  - Identify top 5 predictive features
  - Out-of-sample prediction accuracy

---

**3.3: Scenario Analysis**
*Under different demographic/economic scenarios, what are the enrollment projections?*

- **Scenarios:**
  - Optimistic: Economic growth + increased funding + demographic recovery
  - Baseline: Current trends continue
  - Pessimistic: Economic recession + continued demographic decline + funding cuts

- **Deliverable:**
  - Enrollment range forecasts for each state
  - Identify states most at risk under pessimistic scenario
  - Policy recommendations for at-risk states

---

## Research Design Summary

### Phase 1: Descriptive Analysis (Current Stage)
- 1.1, 1.2, 1.3
- Establish baseline patterns
- Statistical significance testing
- **Deliverable:** Comprehensive EDA report with statistical rigor

### Phase 2: Explanatory Variable Acquisition
- Gather demographic data (Census, NCES)
- Gather economic data (BLS, BEA, SHEEO)
- Gather policy data (State Higher Ed Executive Officers)
- Merge and clean expanded dataset

### Phase 3: Explanatory Analysis
- 2.1, 2.2, 2.3, 2.4
- Correlation and regression analysis
- Identify key drivers
- **Deliverable:** Driver analysis report with policy implications

### Phase 4: Predictive Modeling (Optional)
- RQ3.1, 3.2, 3.3
- Build and validate forecasting models
- **Deliverable:** Enrollment forecasts with confidence intervals