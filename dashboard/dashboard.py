import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
def load_data():
    return pd.read_csv('main_data.csv')

# Helper function to filter data by date range
def filter_data_by_date(df, start_date, end_date):
    df['datetime'] = pd.to_datetime(df['datetime'])  # Convert to datetime
    return df[(df['datetime'] >= pd.to_datetime(start_date)) & (df['datetime'] <= pd.to_datetime(end_date))]

# Load data
df = load_data()

# Streamlit Dashboard UI
st.title("Air Quality Data Analyze by Made Vidyatma Adhi Krisna")

# Sidebar for Date Input
st.sidebar.header("Filter Data by Date")
start_date = st.sidebar.date_input("From", pd.to_datetime("2013-03-01"), min_value=pd.to_datetime("2013-03-01"), max_value=pd.to_datetime("2017-02-28"))
end_date = st.sidebar.date_input("Until", pd.to_datetime("2017-02-28"), min_value=pd.to_datetime("2013-03-01"), max_value=pd.to_datetime("2017-02-28"))

# Filter the dataset based on date input
filtered_df = filter_data_by_date(df, start_date, end_date)

# Create tabs for each question
tab1, tab2 = st.tabs(["Pertanyaan 1", "Pertanyaan 2"])

# Tab 1: Answer to Question 1 (Rata-rata Konsentrasi PM2.5)
with tab1:
    st.subheader("Bagaimana Rata-rata Konsentrasi PM2.5 per Quartal?")
    
    # Add quartal column to the filtered dataset
    filtered_df.loc[:, 'quartal'] = np.select(
        [
            filtered_df['month'].isin([1, 2, 3]),   # Q1
            filtered_df['month'].isin([4, 5, 6]),   # Q2
            filtered_df['month'].isin([7, 8, 9]),   # Q3
            filtered_df['month'].isin([10, 11, 12]) # Q4
        ],
        ['Q1', 'Q2', 'Q3', 'Q4'],
        default='unknown'
    )
    
    # Calculate the date range in days
    date_range = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
    
    if date_range < 365:
        # Condition 1: Static graph (less than a year range)
        # Group by station and quartal
        quartal_stats = filtered_df.groupby(['station', 'quartal'])['PM25'].agg(['mean', 'max', 'min']).reset_index()

        # Plot the mean PM2.5 concentration by station and quartal
        fig, ax = plt.subplots(figsize=(14, 7))
        sns.barplot(x='quartal', y='mean', hue='station', data=quartal_stats, ax=ax)
        ax.set_title('Mean PM2.5 Concentration by Station and Quartal')
        ax.set_ylabel('Mean PM2.5')
        ax.set_xlabel('Quartal')
        ax.grid(True)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        st.pyplot(fig)
    
    else:
        # Condition 2: Dynamic graphic showing quartals between start_date and end_date
        # Create a dynamic graphic showing the quartal available between the start date and end date
        available_quartals = pd.date_range(start=start_date, end=end_date, freq='Q').to_period('Q').astype(str)
        st.write("Available Quartals between the selected date range:")
        st.write(", ".join(available_quartals))
        
        # Filter the dataset to include only the available quartals
        filtered_df['quartal_period'] = filtered_df['datetime'].dt.to_period('Q').astype(str)
        dynamic_quartal_stats = filtered_df[filtered_df['quartal_period'].isin(available_quartals)].groupby(['station', 'quartal_period'])['PM25'].agg(['mean', 'max', 'min']).reset_index()
        
        # Plot the dynamic quartal stats
        fig, ax = plt.subplots(figsize=(14, 7))
        sns.lineplot(x='quartal_period', y='mean', hue='station', data=dynamic_quartal_stats, marker='o', ax=ax)
        ax.set_title('Mean PM2.5 Concentration by Station and Quartal Period')
        ax.set_ylabel('Mean PM2.5')
        ax.set_xlabel('Quartal Period')
        ax.grid(True)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        st.pyplot(fig)

        
# Tab 2: Answer to Question 2 (Hubungan PM2.5 dan NO2 dengan Faktor Cuaca)
with tab2:
    st.subheader("Hubungan PM2.5 dan NO2 dengan Faktor Cuaca (Suhu, Tekanan Udara, dan Kecepatan Angin)")
    
    # Pairplot of PM2.5, NO2, TEMP, PRES, WSPM
    fig_pairplot = sns.pairplot(filtered_df[['PM25', 'NO2', 'TEMP', 'PRES', 'WSPM']], diag_kind='kde', markers='o')
    fig_pairplot.fig.suptitle("Pairplot of PM2.5, NO2, TEMP, PRES, WSPM", y=1.02)
    st.pyplot(fig_pairplot)
    
    # Correlation heatmap
    fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
    sns.heatmap(filtered_df[['PM25', 'NO2', 'TEMP', 'PRES', 'WSPM']].corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax_corr)
    ax_corr.set_title("Correlation Heatmap between PM2.5, NO2, TEMP, PRES, WSPM")
    st.pyplot(fig_corr)

