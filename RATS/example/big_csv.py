
# coding: utf-8

# # Creating a super big CSV file

# In[1]:


import pandas as pd
import numpy as np


# In[4]:


pseudo_name = [''.join(map(chr, np.random.randint(65, 91,3))) for i in range( 10 ** 7 )]
pseudo_age = np.random.randint(low = 25, high = 66, size = 10 ** 7)
pseudo_income = np.random.randint(low = 5000, high = 150001, size = 10 ** 7)
pseudo_family_size = np.random.randint(low = 1, high = 6, size = 10 ** 7)
pseudo_highly_educated = np.random.randint(low = 0, high = 2, size = 10 ** 7)


# In[5]:


df = pd.DataFrame({
    'name': pseudo_name, 
    'age': pseudo_age,
    'income': pseudo_income,
    'family_size': pseudo_family_size,
    'pseudo_highly_educated': pseudo_highly_educated,
    })


# In[8]:


df.to_csv('fake_data.csv', encoding = 'utf-8', index = False,)

