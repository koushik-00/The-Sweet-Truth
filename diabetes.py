import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


data = 'diabetes_2.csv'

st.set_page_config(page_title="Diabetes analysis Dashboard", layout="wide")
st.title("The Sweet truth")

df = pd.read_csv(data)


st.subheader("Data Preview")
st.dataframe(df.head())

st.subheader("Summary Statistics")
st.dataframe(df.describe())

# Histograms of key health metrics
st.subheader("Distribution of Key Health Metrics")
fig, ax = plt.subplots(2, 2, figsize=(12, 8))
df[['Age', 'BMI', 'Fasting_Blood_Glucose', 'HbA1c']].hist(bins=20, ax=ax)
plt.tight_layout()
st.pyplot(fig)

# Lifestyle factor distributions
st.subheader("Lifestyle Factor Distributions")
fig2, axs = plt.subplots(1, 3, figsize=(18, 5))
sns.countplot(x='Alcohol_Consumption', data=df, ax=axs[0])
sns.countplot(x='Smoking_Status', data=df, ax=axs[1])
sns.countplot(x='Physical_Activity_Level', data=df, ax=axs[2])
plt.tight_layout()
st.pyplot(fig2)

# Sankey Diagram
st.subheader("Risk Pathway: Age → Glucose → Family History")

# Prepare Sankey data
sankey_data = df.groupby(['Age_Group', 'Glucose_Level', 'Family_History_of_Diabetes']).size().reset_index(name='count')
labels = list(pd.unique(sankey_data['Age_Group'].astype(str))) + \
         list(pd.unique(sankey_data['Glucose_Level'].astype(str))) + \
         list(pd.unique(sankey_data['Family_History_of_Diabetes'].astype(str)))
label_map = {k: v for v, k in enumerate(labels)}

source = sankey_data['Age_Group'].astype(str).map(label_map)
mid = sankey_data['Glucose_Level'].astype(str).map(label_map)
target = sankey_data['Family_History_of_Diabetes'].astype(str).map(label_map)

# Links
links = pd.concat([
    pd.DataFrame({'source': source, 'target': mid, 'value': sankey_data['count']}),
    pd.DataFrame({'source': mid, 'target': target, 'value': sankey_data['count']})
])

fig3 = go.Figure(go.Sankey(
    node=dict(label=labels, pad=20),
    link=dict(source=links['source'], target=links['target'], value=links['value'])
))
st.plotly_chart(fig3, use_container_width=True)

# 
# features = ['BMI', 'HbA1c', 'Blood_Pressure_Systolic', 'Cholesterol_Total', 'Serum_Urate']

# # Assume 'Risk' column exists with categories like 'Diabetic' and 'Non-Diabetic'
# group_means = df.groupby('Risk')[features].mean().T
# group_means.columns = ['Non-Diabetic', 'Diabetic']  # Adjust these if different in your data

# # Plot using matplotlib
# fig, ax = plt.subplots(figsize=(10, 6))
# group_means.plot(kind='bar', ax=ax)
# ax.set_title("Average Health Metrics by Diabetes Risk")
# ax.set_ylabel("Average Value")
# ax.set_xticklabels(group_means.index, rotation=45)
# ax.grid(axis='y')
# plt.tight_layout()

# # Display in Streamlit
# st.title("Health Metrics Comparison by Diabetes Risk")
# st.pyplot(fig)

# Lifestyle habits
df['HbA1c_Level'] = pd.cut(df['HbA1c'], bins=[0, 5.6, 6.4, 15], labels=['Normal', 'Prediabetic', 'Diabetic'])

# Plot parallel categories chart
fig = px.parallel_categories(
    df,
    dimensions=['Smoking_Status', 'Alcohol_Consumption', 'HbA1c_Level', 'Physical_Activity_Level'],
    color=df['HbA1c'],
    color_continuous_scale='Sunsetdark',
    labels={'HbA1c_Level': 'HbA1c Level'}
)

# Streamlit display
st.title("Parallel Categories: Lifestyle vs HbA1c Level")
st.plotly_chart(fig, use_container_width=True)