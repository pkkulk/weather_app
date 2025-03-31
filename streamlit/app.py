# app.py

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import io # Used for capturing df.info() output


st.set_page_config(
    page_title="CSV Data Insights Generator",
    page_icon="📊",
    layout="wide",  
    initial_sidebar_state="expanded"
)


@st.cache_data 
def load_data(uploaded_file):
   
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

def display_basic_eda(df):
    """Displays basic Exploratory Data Analysis results."""
    st.subheader("1. Basic Data Exploration")

    with st.expander("Show Raw Data Sample", expanded=False):
        st.dataframe(df.head())

    with st.expander("Data Dimensions", expanded=False):
        st.write(f"Number of Rows: {df.shape[0]}")
        st.write(f"Number of Columns: {df.shape[1]}")

    with st.expander("Data Types and Non-Null Counts", expanded=False):
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

    with st.expander("Summary Statistics (Numerical Columns)", expanded=False):
      
        numeric_df = df.select_dtypes(include=np.number)
        if not numeric_df.empty:
            st.dataframe(numeric_df.describe())
        else:
            st.info("No numerical columns found for summary statistics.")

    with st.expander("Missing Value Analysis", expanded=True): # Expand this by default
        missing_values = df.isnull().sum()
        missing_values = missing_values[missing_values > 0] # Filter only columns with missing values
        if not missing_values.empty:
            st.write("Columns with Missing Values:")
            st.dataframe(missing_values.reset_index().rename(columns={'index': 'Column', 0: 'Missing Count'}))

         
            fig_missing, ax_missing = plt.subplots(figsize=(10, 6))
            sns.heatmap(df.isnull(), cbar=False, cmap='viridis', ax=ax_missing)
            ax_missing.set_title('Missing Data Pattern Heatmap')
            st.pyplot(fig_missing)
            st.markdown("""
            **Why this is important (Missing Values):**
            * **Data Quality:** Identifies potential issues in data collection or processing.
            * **Imputation Strategy:** Guides decisions on how to handle missing data (e.g., fill with mean/median/mode, drop rows/columns, predictive imputation).
            * **Bias:** Missing data might not be random, potentially introducing bias if not handled carefully.
            * **Model Performance:** Many machine learning models cannot handle missing values directly.
            """)
        else:
            st.success("No missing values found in the dataset!")



st.title("📊 CSV Data Insights Application")
st.markdown("""
Welcome! Upload your CSV file to explore the data and generate key insights relevant
from a Data Engineering and Analytics perspective.
""")


with st.sidebar:
    st.header("⚙️ Settings")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:

    df = load_data(uploaded_file)

    if df is not None:
        st.success(f"Successfully loaded `{uploaded_file.name}`.")

   
        display_basic_eda(df)
        st.divider() 

  
        st.header("💡 Key Data Insights")

    
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
       
        datetime_cols = df.select_dtypes(include=['datetime', 'datetime64[ns]']).columns.tolist()
        if not datetime_cols:
            
            for col in df.select_dtypes(include=['object']).columns:
                try:
                    pd.to_datetime(df[col], errors='raise')
                    datetime_cols.append(col)
                except (ValueError, TypeError):
                    pass


 
        st.subheader("Insight 1: Distribution of Numerical Features")
        if numeric_cols:
            selected_num_col = st.selectbox(
                "Select a numerical column to view its distribution:",
                options=numeric_cols,
                key="dist_num_select"
            )
            if selected_num_col:
                fig_hist = px.histogram(
                    df,
                    x=selected_num_col,
                    title=f"Distribution of '{selected_num_col}'",
                    marginal="box", 
                    template="plotly_white"
                )
                st.plotly_chart(fig_hist, use_container_width=True)
                st.markdown("""
                **Why this is important (Distribution):**
                * **Data Understanding:** Reveals the range, central tendency, skewness, and presence of outliers.
                * **Data Quality Check:** Helps identify unusual patterns or potential data entry errors.
                * **Feature Engineering:** Guides transformations (e.g., log transform for skewed data).
                * **Model Selection:** Some models assume specific data distributions.
                """)
        else:
            st.info("No numerical columns found in the dataset for distribution analysis.")
        st.divider()

      
        st.subheader("Insight 2: Frequency of Categorical Features")
        if categorical_cols:
            selected_cat_col = st.selectbox(
                "Select a categorical column to view its frequency:",
                options=categorical_cols,
                key="freq_cat_select"
            )
            if selected_cat_col:
         
                max_categories_to_show = 25
                counts = df[selected_cat_col].value_counts()
                if len(counts) > max_categories_to_show:
                    st.warning(f"Displaying top {max_categories_to_show} categories out of {len(counts)} for '{selected_cat_col}'.")
                    counts = counts.nlargest(max_categories_to_show)

                fig_bar = px.bar(
                    counts,
                    x=counts.index,
                    y=counts.values,
                    title=f"Frequency of Categories in '{selected_cat_col}'",
                    labels={'x': selected_cat_col, 'y': 'Count'},
                    template="plotly_white"
                )
                fig_bar.update_layout(xaxis_title=selected_cat_col, yaxis_title="Count")
                st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown("""
                **Why this is important (Categorical Frequency):**
                * **Data Understanding:** Shows the prevalence of different categories.
                * **Data Quality:** Helps spot inconsistent labeling (e.g., 'USA', 'U.S.A.') or rare categories.
                * **Imbalance:** Identifies imbalanced classes, which can affect model training.
                * **Feature Engineering:** Guides encoding strategies (e.g., one-hot encoding vs. grouping rare categories).
                """)
        else:
            st.info("No categorical columns found in the dataset for frequency analysis.")
        st.divider()

   
        st.subheader("Insight 3: Correlation Between Numerical Features")
        if len(numeric_cols) >= 2:

            corr_matrix = df[numeric_cols].corr()

      
            fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax_corr)
            ax_corr.set_title('Correlation Matrix of Numerical Features')
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
            plt.tight_layout() # Adjust layout to prevent labels overlapping
            st.pyplot(fig_corr)

            st.markdown("""
            **Why this is important (Correlation):**
            * **Feature Relationships:** Identifies linear relationships between variables (positive or negative).
            * **Redundancy:** High correlation between features might indicate redundancy (multicollinearity), which can be problematic for some models (e.g., linear regression).
            * **Feature Selection:** Can help in selecting features that are highly correlated with a target variable (if applicable) but not highly correlated with each other.
            * **Data Understanding:** Provides deeper insights into how different numerical aspects of the data relate to each other.
            """)
        elif len(numeric_cols) == 1:
             st.info("Only one numerical column found. Correlation analysis requires at least two numerical columns.")
        else:
            st.info("No numerical columns found for correlation analysis.")
        st.divider()

    
        if datetime_cols:
            st.subheader("Insight 4: Time Series Trends (if applicable)")
            selected_dt_col = st.selectbox(
                "Select a date/time column to analyze trends:",
                options=datetime_cols,
                key="ts_dt_select"
            )
        
            try:
                df[selected_dt_col] = pd.to_datetime(df[selected_dt_col])
                resample_freq = st.radio(
                    "Select aggregation frequency:",
                    ('D', 'W', 'M', 'Q', 'Y'), # Daily, Weekly, Monthly, Quarterly, Yearly
                    index=2, # Default to Monthly
                    horizontal=True,
                    key="ts_freq_radio"
                )

                time_series_data = df.set_index(selected_dt_col).resample(resample_freq).size()
                time_series_data = time_series_data.reset_index() # Reset index to plot with Plotly
                time_series_data.columns = [selected_dt_col, 'Count'] # Rename columns for clarity

                if not time_series_data.empty:
                    fig_ts = px.line(
                        time_series_data,
                        x=selected_dt_col,
                        y='Count', # Plotting the count of records over time
                        title=f"Trend over Time (based on '{selected_dt_col}', aggregated by {resample_freq})",
                        markers=True,
                        template="plotly_white"
                    )
                    st.plotly_chart(fig_ts, use_container_width=True)
                    st.markdown(f"""
                    **Why this is important (Time Series):**
                    * **Trend Analysis:** Identifies upward, downward, or cyclical patterns over time.
                    * **Seasonality:** Helps spot recurring patterns within specific periods (e.g., daily, weekly, yearly).
                    * **Anomaly Detection:** Unusual spikes or drops can indicate significant events or data issues.
                    * **Forecasting:** Understanding historical trends is fundamental for predicting future values.
                    * **Data Freshness/Ingestion Monitoring:** Viewing record counts over time can help monitor data pipelines.
                    """)
                else:
                    st.warning(f"Could not generate time series data for column '{selected_dt_col}'.")

            except Exception as e:
                st.error(f"Could not process column '{selected_dt_col}' as datetime: {e}")
        else:
            st.info("No suitable date/time columns detected for time series analysis.")


 
        st.divider()
        st.markdown("--- End of Analysis ---")

else:
    st.info("Awaiting CSV file upload...")


st.markdown("""
---
*Created with Streamlit for Data Engineering & Analytics Insights*
""")