#!/usr/bin/env python
# coding: utf-8

# ### Monthly Revenue Script

# In[1]:


# Import required libraries
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import plotly.offline as pyoff
import plotly.graph_objs as go

get_ipython().run_line_magic('matplotlib', 'inline')


# ##### Initiate a visualization library for notebook

# In[2]:


pyoff.init_notebook_mode()


# In[3]:


tx_data = pd.read_csv('Business_ReviewData_2020.csv')
tx_data.head(10)


# ##### Convert the type of Report Date field from string to datetime

# In[4]:


tx_data['REPORT_DATE'] = pd.to_datetime(tx_data['REPORT_DATE'])


# In[5]:


tx_data['REPORT_DATE'].describe()


# In[6]:


tx_data['Date_YearMonth'] = tx_data['REPORT_DATE'].map(lambda date: 100*date.year + date.month)
print(tx_data.head(10))


# In[7]:


print(tx_data.describe())


# In[8]:


tx_data.groupby('Date_YearMonth')['REVENUE'].sum()


# In[9]:


tx_revenue = tx_data.groupby(['Date_YearMonth'])['REVENUE'].sum().reset_index()
tx_revenue


# #### Create the visualization

# In[10]:


#X and Y axis inputs for Plotly graph. We use Scatter for line graphs
plot_data = [
    go.Scatter(
        x=tx_revenue['Date_YearMonth'],
        y=tx_revenue['REVENUE'],
    )
]

plot_layout = go.Layout(
        xaxis={"type": "category"},
        title='Montly Revenue'
    )
fig = go.Figure(data=plot_data, layout=plot_layout)
pyoff.iplot(fig)


# In[11]:


#using pct_change() function to see monthly percentage change
tx_revenue['MonthlyGrowth'] = tx_revenue['REVENUE'].pct_change()

#showing first 5 rows
tx_revenue.head()


# #### Create a Monthly Revenue Growth Rate

# In[12]:


#visualization - line graph
plot_data = [
    go.Scatter(
        x=tx_revenue.query("Date_YearMonth < 201112")['Date_YearMonth'],
        y=tx_revenue.query("Date_YearMonth < 201112")['MonthlyGrowth'],
    )
]

plot_layout = go.Layout(
        xaxis={"type": "category"},
        title='Montly Growth Rate'
    )

fig = go.Figure(data=plot_data, layout=plot_layout)
pyoff.iplot(fig)


# In[13]:


tx_data.groupby('DIVISION')['REVENUE'].sum().sort_values(ascending=False).astype(int)


# #### Monthly Active Customers

# In[14]:


#creating a new dataframe with division 10 customers
tx_div= tx_data.query("DIVISION=='10'").reset_index(drop=True)
tx_div.head()


# In[15]:


#creating monthly active customers dataframe by counting unique Customer IDs
tx_monthly_active = tx_div.groupby('Date_YearMonth')['FILE_NO'].nunique().reset_index()

#print the dataframe
tx_monthly_active


# In[16]:


#plotting the output
plot_data = [
    go.Bar(
        x=tx_monthly_active['Date_YearMonth'],
        y=tx_monthly_active['FILE_NO'],
    )
]

plot_layout = go.Layout(
        xaxis={"type": "category"},
        title='Monthly Active Customers'
    )


# In[17]:


fig = go.Figure(data=plot_data, layout=plot_layout)

pyoff.iplot(fig)


# In[18]:


tx_monthly_active['FILE_NO'].mean()


# In[19]:


tx_monthly_sales = tx_div.groupby('Date_YearMonth')['PROFIT'].sum().reset_index()
tx_monthly_sales


# In[20]:


plot_data = [
    go.Bar(
        x=tx_monthly_sales['Date_YearMonth'],
        y=tx_monthly_sales['PROFIT'],
    )
]

plot_layout = go.Layout(
        xaxis={"type": "category"},
        title='Monthly Total Profit'
    )


# In[21]:


fig = go.Figure(data=plot_data, layout=plot_layout)
pyoff.iplot(fig)


# In[22]:


tx_monthly_sales['PROFIT'].mean()


# In[23]:


tx_monthly_profit_avg = tx_div.groupby('Date_YearMonth')['REVENUE'].mean().reset_index()
tx_monthly_profit_avg


# In[24]:


plot_data = [
    go.Bar(
        x=tx_monthly_profit_avg['Date_YearMonth'],
        y=tx_monthly_profit_avg['REVENUE'],
    )
]

plot_layout = go.Layout(
        xaxis={"type": "category"},
        title='Monthly Profit Average'
    )
fig = go.Figure(data=plot_data, layout=plot_layout)
pyoff.iplot(fig)


# In[25]:


tx_monthly_profit_avg.REVENUE.mean()


# In[26]:


tx_div.info()


# ### New and Existing Customers

# In[27]:


tx_min_purchase = tx_div.groupby('CUSTOMER_NAME').REPORT_DATE.min().reset_index()
tx_min_purchase.columns = ['CUSTOMER_NAME', 'MinPurchaseDate']


# In[28]:


tx_min_purchase['MinPurchaseYearMonth'] = tx_min_purchase['MinPurchaseDate'].map(lambda date: 100*date.year + date.month)
tx_min_purchase


# In[29]:


tx_div = pd.merge(tx_div, tx_min_purchase, on='CUSTOMER_NAME')
tx_div.head()


# In[30]:


tx_div['CustomerType'] = 'New'
tx_div.loc[tx_div['Date_YearMonth']>tx_div['MinPurchaseYearMonth'], 'CustomerType'] = 'Existing'
tx_div.CustomerType.value_counts()


# In[31]:


tx_div.head()


# In[32]:


tx_customer_type_revenue = tx_div.groupby(['Date_YearMonth', 'CustomerType'])['REVENUE'].sum().reset_index()


# In[33]:


tx_customer_type_revenue.query("Date_YearMonth != 201911 and Date_YearMonth != 202006")


# In[34]:


tx_customer_type_revenue = tx_customer_type_revenue.query("Date_YearMonth != 201911 and Date_YearMonth != 202006")


# In[35]:


plot_data = [
    go.Scatter(
        x=tx_customer_type_revenue.query("CustomerType == 'Existing'")['Date_YearMonth'],
        y=tx_customer_type_revenue.query("CustomerType == 'Existing'")['REVENUE'],
        name = 'Existing'
    ),
    go.Scatter(
        x=tx_customer_type_revenue.query("CustomerType == 'New'")['Date_YearMonth'],
        y=tx_customer_type_revenue.query("CustomerType == 'New'")['REVENUE'],
        name = 'New'
    )
]

plot_layout = go.Layout(
        xaxis={"type": "category"},
        title='New vs Existing'
    )
fig = go.Figure(data=plot_data, layout=plot_layout)
pyoff.iplot(fig)


# In[36]:


tx_customer_ratio = tx_div.query("CustomerType == 'New'").groupby(['Date_YearMonth'])['CUSTOMER_NAME'].nunique()/tx_div.query("CustomerType == 'Existing'").groupby(['Date_YearMonth'])['CUSTOMER_NAME'].nunique() 
tx_customer_ratio = tx_customer_ratio.reset_index()
tx_customer_ratio = tx_customer_ratio.dropna()

tx_div.query("CustomerType == 'New'").groupby(['Date_YearMonth'])['CUSTOMER_NAME'].nunique()


# In[37]:


tx_div.query("CustomerType == 'Existing'").groupby(['Date_YearMonth'])['CUSTOMER_NAME'].nunique()


# In[38]:


plot_data = [
    go.Bar(
        x=tx_customer_ratio.query("Date_YearMonth > 202001 and Date_YearMonth < 202006")['Date_YearMonth'],
        y=tx_customer_ratio.query("Date_YearMonth > 202001 and Date_YearMonth < 202006")['CUSTOMER_NAME'],
    )
]

plot_layout = go.Layout(
        xaxis={"type": "category"},
        title='New Customer Ratio'
    )
fig = go.Figure(data=plot_data, layout=plot_layout)
pyoff.iplot(fig)


# ### Create Signup Data

# In[39]:


tx_min_purchase.head()


# In[40]:


unq_month_year = tx_min_purchase.MinPurchaseYearMonth.unique()
unq_month_year


# In[41]:


def generate_signup_date(year_month):
    signup_date = [el for el in unq_month_year if year_month >= el]
    
    return np.random.choice(signup_date)


# In[42]:


tx_min_purchase['SignupYearMonth'] = tx_min_purchase.apply(lambda row: generate_signup_date(row['MinPurchaseYearMonth']), axis=1)
tx_min_purchase['InstallYearMonth'] = tx_min_purchase.apply(lambda row: generate_signup_date(row['SignupYearMonth']), axis=1)

tx_min_purchase.head()


# In[43]:


channels = ['organic', 'inorganic', 'referral']

tx_min_purchase['AcqChannel'] = tx_min_purchase.apply(lambda x: np.random.choice(channels), axis=1)


# ### Activation Rate

# In[ ]:
tx_activation = tx_min_purchase[tx_min_purchase['MinPurchaseYearMonth'] 
                                == tx_min_purchase['SignupYearMonth']].groupby(
                                    'SignupYearMonth').FILE_NO.count() / tx_min_purchase.groupby(
                                        'SignupYearMonth').FILE_NO.count()

tx_activation = tx_activation.reset_index()
                                 




