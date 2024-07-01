import pandas as pd
import plotly.express as px

# Load the dataset
file_path = '/workspaces/PersonalWeb/Data/May24df.csv'
df = pd.read_csv(file_path)

# Convert the 'Dr' column to numeric, in case it is not
df['Dr'] = pd.to_numeric(df['Dr'], errors='coerce')

# Group by 'Transaction' and sum the 'Dr' values
spending_summary = df.groupby('Transaction')['Dr'].sum()

# Sort the spending summary to get the top 5 spendings
top_spendings = spending_summary.sort_values(ascending=False).head(5).reset_index()

# Create the Plotly bar chart
fig = px.bar(top_spendings, x='Transaction', y='Dr', title='Top 5 Spendings',
             labels={'Transaction': 'Transaction', 'Dr': 'Amount Spent'},
             template='plotly_white')

#save the chart as html
fig.write_html('/workspaces/PersonalWeb/Projects/Personal_Spend/Charts/top5Chart.html')

# Display the chart 
# fig.show()
