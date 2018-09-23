# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 00:51:33 2018

@author: PRATHAMESH PANDIT
"""

# rnaGENEClassifier


# Python version
import sys
print('Python: {}'.format(sys.version))
# scipy
import scipy
print('scipy: {}'.format(scipy.__version__))
# numpy
import numpy
print('numpy: {}'.format(numpy.__version__))
# matplotlib
import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))
# pandas
import pandas
print('pandas: {}'.format(pandas.__version__))
# scikit-learn
import sklearn
print('sklearn: {}'.format(sklearn.__version__))


# Load libraries
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
import warnings



# Load dataset
names = []
for i in range (20531):
    names.append('gene_'+str(i))

dataset = pandas.read_csv(r'C:\Users\PRATHAMESH PANDIT\Desktop\MachineLearningPractice\TumorClassifier\data\data.csv', names=names)
solutionset = pandas.read_csv(r'C:\Users\PRATHAMESH PANDIT\Desktop\MachineLearningPractice\TumorClassifier\data\labels.csv')

# shape
print(dataset.shape)
print(solutionset.shape)



'''
# head
#print(dataset.head(20))

# describe
print(dataset.describe())

# box and whisker plots
dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
plt.show()

# histograms
dataset.hist()
plt.show()

# scatter plot matrix
scatter_matrix(dataset)
plt.show()
'''


X = dataset.values[1:, :]
Y = solutionset.values[:, 1]
#print(X)
#print(Y)


'''
# Split-out validation dataset
array = dataset.values
X = array[:,0:4]
Y = array[:,4]
'''


validation_size = 0.15
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)



# Test options and evaluation metric
scoring = 'accuracy'

warnings.filterwarnings(action='ignore', category=UserWarning)


# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))



# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = model_selection.KFold(n_splits=10, random_state=seed)
	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)



"""
# Implement Voting

ensemble = []
resultsOFVoting = []
warnings.filterwarnings(action='ignore', category=DeprecationWarning)
ensemble = VotingClassifier(models)
resultsOFVoting = model_selection.cross_val_score(ensemble, X_train, Y_train, cv=kfold, scoring=scoring)
msg1 = "Voting Classifier: %f (%f)" % (resultsOFVoting.mean(), resultsOFVoting.std())
print(msg1)

"""


# Compare Algorithms
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()


# Make predictions on validation dataset
print('Choose an Algorithm to make your prediction:')
for name, model in models:
    print(name)
    
choice = input('Enter your choice: ')
best = ''
if choice == 'LR':
    best = LogisticRegression()
elif choice == 'LDA':
    best = LinearDiscriminantAnalysis()
elif choice == 'KNN':
    best = KNeighborsClassifier()
elif choice == 'CART':
    best = DecisionTreeClassifier()
elif choice == 'NB':
    best = GaussianNB()
elif choice == 'SVM':
    best = SVC()

if best != '' :
    best.fit(X_train, Y_train)
    predictions = best.predict(X_validation)
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))

