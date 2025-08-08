#import streamlit as st

import streamlit as st  # ✅ This must come first
import pandas as pd
import plotly.express as px


# Set page config
st.set_page_config(page_title="Pak-Ind War 2025 Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("india_pakistan_conflict.csv")  # replace with your file
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    return df

df = load_data()

# ------------------ Sidebar ------------------ #
st.sidebar.title("Filter by Year")
years = sorted(df['Year'].dropna().unique())
selected_years = st.sidebar.multiselect("Select Year(s):", years, default=years)

df_filtered = df[df['Year'].isin(selected_years)]

# ------------------ Header ------------------ #
st.markdown("<h1 style='text-align: center; color: red;'>🇵🇰 Pak-Ind War 2025 Dashboard 🇮🇳</h1>", unsafe_allow_html=True)
st.markdown("---")

# ------------------ Row 1: Pie Charts ------------------ #
col1, col2 = st.columns(2)

with col1:
    escalation_counts = df_filtered['Escalation Level'].value_counts()
    fig1 = px.pie(values=escalation_counts.values, names=escalation_counts.index,
                  title="Escalation Level Distribution")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    event_type_counts = df_filtered['Event Type'].value_counts()
    fig2 = px.pie(values=event_type_counts.values, names=event_type_counts.index,
                  title="Event Type Distribution")
    st.plotly_chart(fig2, use_container_width=True)

# ------------------ Row 2: Bar Charts ------------------ #
col3, col4 = st.columns(2)

with col3:
    indian_response_counts = df_filtered['Indian Response'].value_counts().head(5)
    fig3 = px.bar(x=indian_response_counts.index, y=indian_response_counts.values,
                  labels={'x': 'Indian Response', 'y': 'Count'},
                  title="Top Indian Responses")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    pakistani_response_counts = df_filtered['Pakistani Response'].value_counts().head(5)
    fig4 = px.bar(x=pakistani_response_counts.index, y=pakistani_response_counts.values,
                  labels={'x': 'Pakistani Response', 'y': 'Count'},
                  title="Top Pakistani Responses")
    st.plotly_chart(fig4, use_container_width=True)

# ------------------ Row 3: Monthly Timeline ------------------ #
st.markdown("### 📅 Monthly Events Timeline")

monthly_data = df_filtered.groupby(df_filtered['Date'].dt.month_name())['Event Description'].count()
monthly_data = monthly_data.reindex([
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
])
fig5 = px.bar(x=monthly_data.index, y=monthly_data.values,
              labels={'x': 'Month', 'y': 'Number of Events'},
              title="Monthly Event Frequency (All Types)")
st.plotly_chart(fig5, use_container_width=True)

# ------------------ Footer ------------------ #
st.markdown("---")
st.markdown("<h5 style='text-align: center; color: gray;'>Made  by Habib</h5>", unsafe_allow_html=True)




