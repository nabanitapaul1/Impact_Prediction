#!/usr/bin/env python
# coding: utf-8

# # * Business Objective *
# #### To predict the impact of the incident 
# 
# 
# 
# 
# 

# In[2]:


# Import Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
import seaborn as sns 
import io
import os


# # * Dataset Details *

# In[4]:


# Import data sets

incident_service  = pd.read_excel("D:\\Project\\ImpactPrediction\\Final\\Incidents_service.xlsx", sheet_name=0)
incident_service


#  # * Exploratory Data Analysis *

# In[111]:


incident_service


# In[112]:


incident_service.head() # Top 5 records


# In[113]:


incident_service.shape # Dimensions of  dataset


# In[114]:


incident_service.dtypes # Data Types of each variable


# In[115]:


incident_service.info()


# In[116]:


incident_service.describe()


# In[117]:


incident_service.describe


# In[118]:


#get only count of unique categories for each variable

for a_feature in incident_service.columns:
    print(len(incident_service[a_feature].unique()))


# In[6]:


#To get only the unique ID of the incidents

uniue_ids = incident_service["ID"].unique()
uniue_ids


# In[7]:


# Checking for null values

incident_service.isnull().sum()


# In[5]:


incident_service[["ID","ID_status","updated_at"]].head(10)


# ## Data Cleaning 

# In[11]:


# sorting data based on ID and updated_at variable

incident_service_sort = incident_service.sort_values(by=["ID","updated_at"])
incident_service_sort[["ID","ID_status","updated_at"]].head(20)


# In[12]:


len(incident_service_sort)


# In[124]:


#incident_service_sort.to_excel("Sorted_incident_data.xlsx") # Importing to excel sorted data


# In[13]:


# Considering only the last entries for each and remove the duplicate values

incident_service2=incident_service_sort.drop_duplicates(subset=['ID','ID_status'],keep='last', inplace=False)

incident_service2.head(20)


# In[14]:


len(incident_service2) 


# In[18]:


# Current Directory
os.getcwd()


# In[19]:


# Set new Directory 
os.chdir("D:\\Project\\ImpactPrediction\\Final")


# In[20]:


incident_service2.to_excel("incident_service_wod.xlsx") # Exporting to excel sorted data without duplicates


# ##  **Visualizations**

# In[22]:


#Impact 

sns.countplot(x="impact", data=incident_service2)


# In[23]:


# id

uniue_ids = incident_service2["ID"].unique()
len(uniue_ids) 


# #### There are total 24918 unique incidents

# In[24]:


# Id_status

incident_service2["ID_status"].value_counts()


# In[25]:


plt.figure(figsize=(16, 6))
sns.countplot(x= "ID_status", data = incident_service2)


# In[132]:


# Active
sns.countplot(x= "active", data = incident_service2)


# In[26]:


# ID Caller

uniue_id_caller = incident_service["ID_caller"].unique()
len(uniue_id_caller)


# In[134]:


plt.figure(figsize=(16, 6))
sns.countplot(x= "ID_caller", data = incident_service2)


# In[27]:


# opened_by

uniue_opened_by = incident_service["opened_by"].unique()
len(uniue_opened_by)


# In[136]:



plt.figure(figsize=(16, 6))
sns.countplot(x= "opened_by", data = incident_service2)


# In[28]:


# created_by

uniue_created_by = incident_service["Created_by"].unique()
len(uniue_created_by)


# In[29]:


plt.figure(figsize=(16, 6))
sns.countplot(x= "Created_by", data = incident_service2)


# In[30]:


# Updated By
uniue_updated_by = incident_service["updated_by"].unique()
len(uniue_updated_by)


# In[140]:


plt.figure(figsize=(16, 6))
sns.countplot(x= "updated_by", data = incident_service2)


# In[141]:


plt.figure(figsize=(16, 6))
sns.countplot(x="type_contact",data= incident_service2)


# In[142]:


incident_service2.dtypes


# In[32]:


incident_service_updated = incident_service2[["ID_status","active","ID_caller","opened_by","Created_by","updated_by",
                                                   "type_contact","location","category_ID",
                                                   "user_symptom","impact",
                                                   "Support_group","support_incharge",
                                                   "Doc_knowledge","confirmation_check","notify","problem_id","change request"]]


# In[33]:


incident_service_updated.head(10)


# In[34]:


incident_service_updated.dtypes


# In[35]:


incident_service_updated.shape


# In[36]:


# Chi Square test result

target = incident_service_updated["impact"]
target.shape
features = incident_service_updated.drop(["impact"],axis=1)
from scipy.stats import chi2_contingency
#from scipy.stats import chi2

features.shape

def Chi_Square_test():
    Chi_test_result =  pd.DataFrame()
    feature_name = []
    pvalue = []
    significant = []
    for a_feature in features.columns:
        data_crosstab = pd.crosstab([incident_service_updated[a_feature]],  
                             incident_service_updated.impact, margins = False)
        xsq,p_value,dof,expected = chi2_contingency(data_crosstab)
            
        feature_name.append(a_feature)
        pvalue.append(p_value)
        if p_value < 0.05:
            a_decision = "Yes"
            significant.append(a_decision)
        else:
            a_decision = " No"
            significant.append(a_decision)
 
    Chi_test_result["feature_names" ]= feature_name
    Chi_test_result["P-Values"] = pvalue
    Chi_test_result["Significant"] = significant
    print(Chi_test_result)
    

Chi_Square_test()


# In[39]:



incident_service_new = incident_service_updated.drop(["active","notify"],axis=1)

incident_service_new


# In[51]:



#Deleting the records for ID_status =-100
incident_service_new = incident_service_new.drop(incident_service_new[incident_service_new.ID_status== -100].index)
incident_service_new


# In[41]:


print(incident_service_new["ID_status"].value_counts())


# In[42]:


# Converting Categorical variables to numerical Variables
# Label Encoding

from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
for a_feature in incident_service_new.columns:
    #print(a_feature)
    incident_service_new[a_feature]= label_encoder.fit_transform(incident_service_new[a_feature]) 


# In[43]:


incident_service_new


# In[45]:


incident_service_new.to_excel("encoded.xlsx")


# In[44]:


os.getcwd()


# In[46]:


incident_service_new.dtypes


# In[47]:


incident_service_new.corr()


# In[50]:


# Increase the size of the heatmap.
plt.figure(figsize=(16, 6))
# Store heatmap object in a variable to easily access it when you want to include more features (such as title).
# Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
heatmap = sns.heatmap(incident_service_new.corr(), vmin=-1, vmax=1, annot=True,cmap='BrBG')
# Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12);


# In[53]:


#Droping faeautures like "problem_id" and "change_request"

incident_service_final = incident_service_new.drop(["problem_id","change request"], axis=1)
incident_service_final.dtypes


# ## Data partitioning 

# In[54]:



from sklearn.model_selection import train_test_split 

features = incident_service_final.drop(["impact"], axis=1)
target = incident_service_final["impact"]

features.shape, target.shape


# In[55]:


train, test = train_test_split(incident_service_final, test_size =0.3, random_state = np.random )
len(train), len(test)  # Size of trian and test


# In[56]:


# Exporting train and test data to excel
train.to_excel("train_incident_prediction.xlsx"), test.to_excel("test_incident_prediction.xlsx")


# In[162]:


train.shape, test.shape


# In[57]:



# checeking value counts for impact variables in train datasets

train['impact'].value_counts()


# In[58]:



plt.figure(figsize=(10, 7))
train_plot_impact = sns.countplot(x= "impact", data = train)
train_plot_impact.set_title('Different categories of Impact Variable', fontsize=20)


for p in train_plot_impact.patches:
    train_plot_impact.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
plt.show()


# In[165]:


# pip install imblearn


# In[60]:


# Balancing Imbalance dataset

from imblearn.over_sampling import SMOTE
from collections import Counter

x_train = train.drop(["impact"],axis=1)
y_train = train["impact"]
#x_train.shape, y_train.shape

oversample = SMOTE()
x_train_new, y_train_new = oversample.fit_resample(x_train, y_train)
#balance_data = x_train_new
#balance_data["impact"] = y_train_new
#balance_data.columns
#balance_data.to_excel("incident_balance_data.xlsx")

x_train_new.shape, y_train_new.shape


# In[61]:


# summarize distribution of target variable of train
counter = Counter(y_train_new)
for k,v in counter.items():
	per = v / len(y_train_new) * 100
	print('Class=%d, n=%d (%.3f%%)' % (k, v, per))
    
# plot the distribution
from matplotlib import pyplot 
pyplot.bar(counter.keys(), counter.values(), color = "Green",edgecolor= "Black" )
pyplot.show()


# In[168]:


#y_train_new.to_excel("y_train.xlsx")


# In[64]:


#Spliting the test data into feature and target variable
x_test = test.drop(["impact"],axis=1)
y_test = test["impact"]
x_test.shape, y_test.shape


# # * Model Building *
# 
# 

# In[65]:


#1. Decision Tree

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Defining model
model_dt = DecisionTreeClassifier()

# fit the model with training data
model_dt.fit(x_train_new,y_train_new)

# depth of the decision tree
print("Depth of the decision tree: ", model_dt.get_depth())
model_dt
# predict the target on train data
predict_train = model_dt.predict(x_train_new)
predict_train


# Accuracy on train data 
Accu_train_dt = accuracy_score(y_train_new,predict_train)


# predict the target on test data
predict_test = model_dt.predict(x_test)

# predict_test

# Accuracy score on test data
Accu_test_dt = accuracy_score(y_test,predict_test)
print("Decisison tree model is made")


# In[66]:


Accu_train_dt, Accu_test_dt


# In[67]:


# Classification Report for Decision tree

from sklearn.metrics import classification_report

des_tree_report = classification_report(y_test,predict_test, output_dict=True)

des_tree_report =pd.DataFrame(des_tree_report).transpose()
des_tree_report


# In[173]:


# 2  Support Vector Machine

from sklearn.svm import SVC

# Defining svc model 
#model_svm =SVC()
#model_svm.fit(x_train_new,y_train_new)


# fit the model with training data
#model_svm.fit(x_train_new,y_train_new)


#model_svm

# predict the target on train data

#predict_train = model_svm.predict(x_train_new)
#predict_train


# Accuracy on train data 
#Accu_train_svm = accuracy_score(y_train_new,predict_train)


# predict the target on test data
#predict_test = model_svm.predict(x_test)

# predict_test

# Accuracy score on test data
#Accu_test_svm = accuracy_score(y_test,predict_test)

#Accu_train_svm, Accu_test_svm


# In[174]:


#Accu_train_svm, Accu_test_svm


# In[68]:


# 3. k-nearest neighbour
from sklearn.neighbors import KNeighborsClassifier
model_knn =  KNeighborsClassifier()
model_knn.fit(x_train_new,y_train_new)

print('\nThe number of neighbors used to predict the target : ',model_knn.n_neighbors)

# predict the target on train data
predict_train = model_knn.predict(x_train_new)
predict_train


# Accuracy on train data 
Accu_train_knn = accuracy_score(y_train_new,predict_train)


# predict the target on test data
predict_test = model_knn.predict(x_test)

# predict_test

# Accuracy score on test data
Accu_test_knn = accuracy_score(y_test,predict_test)

Accu_train_knn, Accu_test_knn


# In[69]:


# Classification Report for KNN


knn_report = classification_report(y_test,predict_test, output_dict=True)
knn_report =pd.DataFrame(des_tree_report).transpose()
knn_report


# In[70]:



# 4. Random Forest

from sklearn.ensemble import RandomForestClassifier

# Defining reandom forest model
model_rf = RandomForestClassifier()
model_rf.fit(x_train_new,y_train_new)


print('Number of trees used : ',model_rf.n_estimators)

# predict the target on train data
predict_train = model_rf.predict(x_train_new)
predict_train


# Accuracy on train data 
Accu_train_rf = accuracy_score(y_train_new,predict_train)


# predict the target on test data
predict_test = model_rf.predict(x_test)

# predict_test

# Accuracy score on test data
Accu_test_rf = accuracy_score(y_test,predict_test)

Accu_train_rf, Accu_test_rf, print('Number of trees used : ',model_rf.n_estimators)


# In[71]:


# Classification Report for Random Forest


rf_report = classification_report(y_test,predict_test, output_dict=True)
rf_report =pd.DataFrame(des_tree_report).transpose()
rf_report


# In[72]:


# 5. Gradient Boosting 

from sklearn.ensemble import GradientBoostingClassifier 

# Defining model
model_gbm =  GradientBoostingClassifier(n_estimators = 100, max_depth = 5)
model_gbm.fit(x_train_new,y_train_new)

# predict the target on train data
predict_train = model_rf.predict(x_train_new)
predict_train

# Accuracy on train data 
Accu_train_gbm = accuracy_score(y_train_new,predict_train)

# predict the target on test data
predict_test = model_gbm.predict(x_test)

# predict_test

# Accuracy score on test data
Accu_test_gbm = accuracy_score(y_test,predict_test)

Accu_train_gbm, Accu_test_gbm,


# In[73]:


# Classification Report for Gradient Boosting

gb_report = classification_report(y_test,predict_test, output_dict=True)
gb_report =pd.DataFrame(des_tree_report).transpose()
gb_report


# In[74]:


# 6.  XG Boosting

from xgboost import XGBClassifier

model_xgb = XGBClassifier()
model_xgb.fit(x_train_new,y_train_new)

# predict the target on train data
predict_train = model_xgb.predict(x_train_new)
predict_train

# Accuracy on train data 
Accu_train_xgb = accuracy_score(y_train_new,predict_train)

# predict the target on test data
predict_test = model_xgb.predict(x_test)

# predict_test

# Accuracy score on test data
Accu_test_xgb = accuracy_score(y_test,predict_test)

Accu_train_xgb, Accu_test_xgb


# In[75]:


# Classification report for XG Boost

xgb_report = classification_report(y_test,predict_test, output_dict=True)
xgb_report =pd.DataFrame(des_tree_report).transpose()
xgb_report


# # * Model Evaluation *

# In[77]:


#model building Results

Overall_results = {"Model":pd.Series(["Decision Tree","KNN","Random Forest","GBM", "XGBoost"]),"Train_accuracy":pd.Series([Accu_train_dt, Accu_train_knn, Accu_train_rf,Accu_train_gbm,Accu_train_xgb]), "Test_accuracy":pd.Series([Accu_test_dt, Accu_test_knn, Accu_test_rf,Accu_test_gbm,Accu_test_xgb])}
Overall_results =pd.DataFrame(Overall_results)
Overall_results


# ## Further Research
# #### Dataset that is provided have lot of categorical variables and each categorical variables 
# #### have very high cardinality, So its better to go and train with Catboost Model which is very efficient 
# #### in   dealing with high cardinality   categorical variable.
# 

# In[80]:



incident_service_new.columns

   


# In[81]:


incident_service_updated.dtypes


# In[83]:


incident_service_catboost= incident_service_updated.drop(incident_service_updated[incident_service_updated.ID_status== -100].index)

incident_service_catboost = incident_service_catboost.drop(["active","notify","problem_id",
                                                           "change request"],axis=1)
incident_service_catboost.columns


# In[85]:


incident_service_catboost.ID_status.value_counts()


# In[188]:


# Import label encoder 
#from sklearn import preprocessing 
  
# label_encoder object knows how to understand word labels. 
#label_encoder = preprocessing.LabelEncoder() 
  
# Encode labels in column 'species'. 
#incident_service_catboost['impact']= label_encoder.fit_transform(incident_service_catboost['impact']) 
  
#incident_service_catboost['impact'].unique()


# In[86]:


# train test split

from sklearn.model_selection import train_test_split 

features_catboost = incident_service_catboost.drop(["impact"], axis=1)
target_catboost = incident_service_catboost["impact"]

features_catboost.shape, target_catboost.shape

X_train_catboost, X_validation_catboost, y_train_catboost, y_validation_catboost = train_test_split(features_catboost, target_catboost, train_size=0.7, random_state=1234)
X_train_catboost.shape, X_validation_catboost.shape, y_train_catboost.shape, y_validation_catboost.shape


# In[87]:


X_train_catboost.dtypes


# In[89]:


categorical_features_indices = np.where(X_train_catboost.dtypes != np.float)[0]
categorical_features_indices


# In[90]:


from catboost import CatBoostClassifier

model_catboost = CatBoostClassifier(iterations=100,
                           learning_rate=1,
                           random_state= 2021,
                           eval_metric='Accuracy')

model_catboost.fit(X_train_catboost, y_train_catboost, cat_features = categorical_features_indices, plot=True,
         eval_set=(X_validation_catboost,y_validation_catboost))


# In[91]:


from sklearn import metrics 


y_pred_catboost_train =  model_catboost.predict(X_train_catboost)
accuracy_score_train = metrics.accuracy_score(y_train_catboost,y_pred_catboost_train)
accuracy_score_train


# In[92]:


y_pred_catboost = model_catboost.predict(X_validation_catboost)
y_pred_catboost


# In[93]:


a_df = pd.DataFrame(y_pred_catboost, columns = ["Impact"])
a_df["Impact"].value_counts()


# In[94]:



accuracy_score_test= metrics.accuracy_score(y_validation_catboost,y_pred_catboost)
accuracy_score_train, accuracy_score_test


# In[197]:


# Classification report for Catboost

catboost_report = classification_report(y_validation_catboost,y_pred_catboost, output_dict=True)
catboost_report =pd.DataFrame(catboost_report).transpose()
catboost_report


# In[95]:


incident_service_catboost.columns


# In[96]:


incident_service_catboost["ID_caller"].value_counts()


# In[97]:


caller_id=pd.DataFrame(incident_service_catboost['ID_caller'].value_counts().index)
caller_id


# In[98]:


features_catboost = incident_service_catboost.drop(["impact"], axis=1)
features_catboost.columns


# In[99]:


caller_id.to_csv("CallerID.csv", index=False, header=False)


# In[100]:


#incident_service_catboost["ID_caller"].value_counts()

for a_feature in features_catboost.columns:
    a_feature_categories=pd.DataFrame(features_catboost[a_feature].value_counts().index)
    file_name = a_feature+ ".csv"
    a_feature_categories.to_csv(file_name, index=False, header=False)


# # * Deployment *

# #### Creating Pickle file
# 

# In[111]:


import pickle


# In[112]:


os.chdir("D:\\Project\\ImpactPrediction\\Final\\Deployment")


# In[113]:


# Saving model to  disk
pickle.dump(model_catboost,open('model.pkl','wb'))


# In[114]:


# Loading model to compare the results
model = pickle.load(open("model.pkl","rb"))


# In[115]:


model


# In[117]:


output = model.predict(X_validation_catboost)
output


# In[118]:


output = pd.DataFrame(output)


# In[119]:


output


# In[121]:


print(output[0].value_counts())


# In[122]:


model.predict([["New","Caller 3763","Opened by 501","Created by 89","Updated by 533","Phone","Location 54","Category 31","Symptom 70","Group 21","Resolver 229","True", "False"]])


# In[123]:


predicted_value = model.predict([["New","Caller 1283","Opened by 59","Created by 108","Updated by 723","Phone","Location 33","Category 36","Symptom 587","Group 17","Resolver 84", "True", "False"]])


# In[124]:


type(predicted_value)


# In[125]:


print(predicted_value.item(0)) 


# In[126]:


type(X_validation_catboost)


# In[127]:


X_validation_catboost.to_csv("Validation_catboost.csv", index=False, header=False)


# In[128]:


output.to_csv("predicted_catboost.csv",index=False,header=False)


# In[131]:


pv= model.predict([["New","Caller 4271","Opened by  131","Created by 62", "Updated by 135","Phone","Location 91","Category 53",	"Symptom 126",	"Group 24","Resolver 132","TRUE","FALSE" ]])


# In[134]:


print(pv[0][0])

