#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import os


# In[4]:


pwd = os.getcwd()


# In[9]:


dataset = pd.read_excel(pwd + "/Data - Survey Monkey Output Edited.xlsx", sheet_name="Edited_Data")
dataset


# In[31]:


dataset_modified = dataset.copy()
dataset_modified


# In[32]:


columns_to_drop = ['Start Date', 'End Date', 'Email Address', 'First Name', 'Last Name', 'Custom Data 1']
columns_to_drop


# In[33]:


dataset_modified = dataset_modified.drop(columns=columns_to_drop)
dataset_modified


# In[34]:


id_vars = list(dataset_modified.columns)[ : 8]
value_vars = list(dataset_modified.columns)[8 : ]
# value_vars


# In[35]:


dataset_melted = dataset_modified.melt(id_vars=id_vars, value_vars = value_vars, var_name="Question + Subquestion", value_name="Answer")
dataset_melted


# In[39]:


questions_import = pd.read_excel(pwd + "/Data - Survey Monkey Output Edited.xlsx", sheet_name="Question")
questions_import


# In[42]:


questions = questions_import.copy()
questions.drop(columns=["Raw Question", "Raw Subquestion", "Subquestion"], inplace=True)


# In[43]:


questions


# In[46]:


questions.dropna(inplace=True)


# In[48]:


questions


# In[49]:


dataset_merged = pd.merge(left=dataset_melted, right=questions, how="left", left_on="Question + Subquestion", right_on="Question + Subquestion")
print("Original Data", len(dataset_melted))
print("Merged Data", len(dataset_merged))
dataset_merged


# In[63]:


respondents = dataset_merged[dataset_merged["Answer"].notna()]
respondents = respondents.groupby("Question")["Respondent ID"].nunique().reset_index()
respondents.rename(columns={"Respondent ID":"Respondents"}, inplace=True)
respondents


# In[64]:


dataset_merged_two = pd.merge(left=dataset_merged, right=respondents, how="left", left_on="Question", right_on="Question")
print("Original Data", len(dataset_merged))
print("Merged Data", len(dataset_merged_two))
dataset_merged_two


# In[65]:


same_answer = dataset_merged # [dataset_merged["Answer"].notna()]
same_answer = same_answer.groupby(["Question + Subquestion", "Answer"])["Respondent ID"].nunique().reset_index()
same_answer.rename(columns={"Respondent ID":"Same Answer"}, inplace=True)
same_answer


# In[67]:


dataset_merged_three = pd.merge(left=dataset_merged_two, right=same_answer, how="left", left_on=["Question + Subquestion", "Answer"], right_on=["Question + Subquestion", "Answer"])
dataset_merged_three["Same Answer"].fillna(0, inplace=True)
print("Original Data", len(dataset_merged_two))
print("Merged Data", len(dataset_merged_three))
dataset_merged_three


# In[68]:


output = dataset_merged_three.copy()
output.rename(columns={"Identify which division you work in. - Response":"Division Primary", "Identify which division you work in. - Other (please specify)":"Division Secondary", "Which of the following best describes your position level? - Response":"Position", "Which generation are you apart of? - Response":"Generation", "Please select the gender in which you identify. - Response":"Gender", "Which duration range best aligns with your tenure at your company? - Response":"Tenure", "Which of the following best describes your employment type? - Response":"Employment Type"}, inplace=True)
output


# In[69]:


output.to_excel(pwd + "/Final_Output.xlsx", index=False)


# In[ ]:




