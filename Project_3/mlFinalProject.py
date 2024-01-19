from tabulate import tabulate
import matplotlib.pyplot as plt
import sklearn.tree as tree
import pandas as pd
from sklearn import linear_model
# from sklearn.base import r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.metrics import jaccard_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import confusion_matrix, accuracy_score
import sklearn.metrics as metrics
import pyreadr

path='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillUp/labs/ML-FinalAssignment/Weather_Data.csv'
df = pd.read_csv(path)
df.head()
df.to_csv('Weather_Data.csv')
df.columns
df = pd.read_csv("Weather_Data.csv")
df.head() 
df.drop(columns='Unnamed: 0', axis=1)


df_sydney_processed = pd.get_dummies(data=df, columns=['RainToday', 'WindGustDir', 'WindDir9am', 'WindDir3pm'])
df_sydney_processed.replace(['No', 'Yes'], [0,1], inplace=True)
df_sydney_processed.drop('Date',axis=1,inplace=True)
df_sydney_processed = df_sydney_processed.astype(float)
features = df_sydney_processed.drop(columns='RainTomorrow', axis=1)
Y = df_sydney_processed['RainTomorrow']


x_train, x_test, y_train, y_test = train_test_split(features, Y, test_size=0.2, random_state=10)
x_train.shape
x_test.shape
y_train.shape
y_test.shape

# Q2) Create and train a Linear Regression model called LinearReg using the training data (x_train, y_train).
linearReg = LinearRegression()
linearReg.fit(x_train, y_train)

# Q3) Now use the predict method on the testing data (x_test) and save it to the array predictions.
prediction = linearReg.predict(x_test)
prediction[0:4]


# Q4) Using the predictions and the y_test dataframe calculate the value for each metric using the appropriate function.
LinearRegression_MAE = np.mean(np.absolute(prediction - y_test))
LinearRegression_MSE = np.mean((prediction - y_test)**2)
LinearRegression_R2 = r2_score(prediction, y_test)
# Q5) Show the MAE, MSE, and R2 in a tabular format using data frame for the linear model.
dict = [["LinearRegression_MAE",LinearRegression_MAE],["LinearRegression_MSE",LinearRegression_MSE],
       ["LinearRegression_R2",LinearRegression_R2]]
Report = pd.DataFrame(dict)
tabulate(Report)

# Q6) Create and train a KNN model called KNN using the training data (x_train, y_train) with the n_neighbors parameter set to 4.
KNN = KNeighborsClassifier(n_neighbors=4).fit(x_train, y_train)
# Q7) Now use the predict method on the testing data (x_test) and save it to the array predictions.
predictions = KNN.predict(x_test)
predictions[0:4]

# Q8) Using the predictions and the y_test dataframe calculate the value for each metric using the appropriate function.
KNN_Accuracy_Score = accuracy_score(y_test, predictions)
KNN_JaccardIndex = jaccard_score(y_test, predictions, average='weighted')
KNN_F1_Score = f1_score(y_test, predictions)

# ---- Decision Tree
# Q9) Create and train a Decision Tree model called Tree using the training data (x_train, y_train).
Tree = DecisionTreeClassifier(criterion='entropy', max_depth=4)
Tree.fit(x_train, y_train)
predictions = Tree.predict(x_test)
predictions[0:4]
y_test[0:4]

print("Decision Tree Accuracy: {}".format(accuracy_score(y_test, predictions)))

tree.plot_tree(Tree)
plt.show()

# Q11) Using the predictions and the y_test dataframe calculate the value for each metric using the appropriate function.
Tree_Accuracy_Score = accuracy_score(y_test, predictions)
Tree_JaccardIndex = jaccard_score(y_test, predictions, average='weighted')
Tree_F1_Score = f1_score(y_test, predictions)

print("Tee Accuracy Score %.2f" % Tree_Accuracy_Score)
print("Tee Jaccard Index %.2f" % Tree_JaccardIndex)
print("Tee F1 Score %.2f" % Tree_F1_Score)

# ------ Logistic Regression
# Q12) Use the train_test_split function to split the features and Y dataframes with a test_size of 0.2 and the random_state set to 1
x_train, x_test, y_train, y_test = train_test_split(features, Y, random_state=1)
# Q13) Create and train a LogisticRegression model called LR using the training data (x_train, y_train) with the solver parameter set to liblinear.
LR = LogisticRegression(C=0.001, solver='liblinear').fit(x_train, y_train)
# Q14) Now, use the predict and predict_proba methods on the testing data (x_test) and save it as 2 arrays predictions and predict_proba
predictions = LR.predict(x_test)
predictions_proba = LR.predict_proba(x_test)

# Q15) Using the predictions, predict_proba and the y_test dataframe calculate the value for each metric using the appropriate function.
LR_Accuracy_Score = accuracy_score(y_test, predictions)
LR_JaccardIndex = jaccard_score(y_test, predictions, average='weighted')
LR_F1_Score = f1_score(y_test, predictions)
LR_Log_Loss = log_loss(y_test, predictions)


# --- SVM
# Q16) Create and train a SVM model called SVM using the training data (x_train, y_train).
SVM = svm.SVC(kernel='rbf')
SVM.fit(x_train, y_train)
# Q17) Now use the predict method on the testing data (x_test) and save it to the array predictions
predictions = SVM.predict(x_test)

SVM_Accuracy_Score =  accuracy_score(y_test, predictions)
SVM_JaccardIndex = jaccard_score(y_test, predictions)
SVM_F1_Score = f1_score(y_test, predictions, average='weighted')

print("Tee Accuracy Score %.2f" % SVM_Accuracy_Score)
print("Tee Jaccard Index %.2f" % svm)
print("Tee F1 Score %.2f" % Tree_F1_Score)


dict1 = {'LinearRegression' : [LinearRegression_MAE,LinearRegression_MSE,LinearRegression_R2],
         'KNN' : [KNN_Accuracy_Score,KNN_JaccardIndex,KNN_F1_Score],
         'DecisionTree' : [Tree_Accuracy_Score,Tree_JaccardIndex,Tree_F1_Score],
         'LogisticRegression' : [LR_Accuracy_Score,LR_JaccardIndex,LR_F1_Score],
         'SVM' : [SVM_Accuracy_Score,SVM_JaccardIndex,SVM_F1_Score]
        }
dict2 = [["LinearRegression_MAE",LinearRegression_MAE],["LinearRegression_MSE",LinearRegression_MSE],
         ["LinearRegression_R2",LinearRegression_R2],
         ["KNN_Accuracy_Score",KNN_Accuracy_Score],["KNN_JaccardIndex",KNN_JaccardIndex],
         ["KNN_F1_Score",KNN_F1_Score],
         ["Tree_Accuracy_Score",Tree_Accuracy_Score],["Tree_JaccardIndex",Tree_JaccardIndex],
         ["Tree_F1_Score",Tree_F1_Score],
         ["LR_Accuracy_Score",LR_Accuracy_Score],["LR_JaccardIndex",LR_JaccardIndex],
         ["LR_F1_Score",LR_F1_Score],["LR_log_Loss",LR_Log_Loss],
         ["SVM_Accuracy_Score",SVM_Accuracy_Score],["SVM_JaccardIndex",SVM_JaccardIndex],
         ["SVM_F1_Score",SVM_F1_Score]]
Report = pd.DataFrame(data=dict2)
print(tabulate(Report))