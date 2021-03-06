#####################
#	import packages
#####################
import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from sklearn.metrics import precision_score, recall_score, accuracy_score, roc_curve, auc, precision_recall_curve
from skopt import BayesSearchCV
from sklearn.model_selection import StratifiedKFold, RepeatedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot as pl

#####################
#	import the data
#####################
#import the data to be used (import feature selection datasets if using those)
X_train = pd.read_csv('X_train.txt', sep="\t", header= 0, index_col=0)
X_test = pd.read_csv('X_test.txt', sep="\t", header= 0, index_col=0)
y_train = pd.read_csv('y_train.txt', sep="\t", header= 0, index_col=0)
y_test = pd.read_csv('y_test.txt', sep="\t", header= 0, index_col=0)
y_train = y_train.values.ravel()
y_test = y_test.values.ravel()



###########
# Tune the model
###########

def status_print(optim_result):
    """Status callback during bayesian hyperparameter search"""
    
    # Get all the models tested so far in DataFrame format
    all_models = pd.DataFrame(bayes_cv_tuner.cv_results_)    
    
    # Get current parameters and the best parameters    
    best_params = pd.Series(bayes_cv_tuner.best_params_)
    print('Model #{}\nBest pr-AUC: {}\nBest params: {}\n'.format(
        len(all_models),
        np.round(bayes_cv_tuner.best_score_, 4),
        bayes_cv_tuner.best_params_
    ))


bayes_cv_tuner = BayesSearchCV(
    estimator = RandomForestClassifier(random_state=10,  class_weight='balanced'),
    search_spaces = {
        'max_depth': (2, 15, 'uniform'),
        'min_samples_leaf': (1, 15, 'uniform')
    },    
    cv = StratifiedKFold(
        n_splits=5,
        shuffle = True,
        random_state=15
    ),
    n_jobs = 2,
    n_iter = 100,
    verbose = 0,
    refit = True,
    random_state = 5,
    scoring = 'average_precision'
)

result = bayes_cv_tuner.fit(X_train, y_train, callback=status_print)


#put the parameters into the next model to tune next parameters
bayes_cv_tuner = BayesSearchCV(
    estimator = RandomForestClassifier(random_state=10,  class_weight='balanced', max_depth = , min_samples_leaf = ),
    search_spaces = {
        'n_estimators': (10, 5000, 'uniform')
    },    
    cv = StratifiedKFold(
        n_splits=5,
        shuffle = True,
        random_state=15
    ),
    n_jobs = 2,
    n_iter = 100,
    verbose = 0,
    refit = True,
    random_state = 5,
    scoring = 'average_precision'
)

result = bayes_cv_tuner.fit(X_train, y_train, callback=status_print)



bayes_cv_tuner = BayesSearchCV(
    estimator = RandomForestClassifier(random_state=10,  class_weight='balanced', max_depth = , min_samples_leaf = , n_estimators = ),
    search_spaces = {
        'min_samples_split': (2, 150, 'uniform')
    },    
    cv = StratifiedKFold(
        n_splits=5,
        shuffle = True,
        random_state=15
    ),
    n_jobs = 2,
    n_iter = 50,
    verbose = 0,
    refit = True,
    random_state = 5,
    scoring = 'average_precision'
)

result = bayes_cv_tuner.fit(X_train, y_train, callback=status_print)




#try out max_features of log2 and sqrt
estimator = RandomForestClassifier(random_state=10,  class_weight='balanced', max_depth = , min_samples_leaf = , n_estimators = , min_samples_split = , max_features = 'log2')
np.mean(cross_val_score(estimator, X_train, y_train, cv = StratifiedKFold(n_splits=5, shuffle = True, random_state=15), scoring = 'average_precision'))

estimator = RandomForestClassifier(random_state=10,  class_weight='balanced', max_depth = , min_samples_leaf = , n_estimators = , min_samples_split = , max_features = 'sqrt')
np.mean(cross_val_score(estimator, X_train, y_train, cv = StratifiedKFold(n_splits=5, shuffle = True, random_state=15), scoring = 'average_precision'))


clf = RandomForestClassifier(random_state=10,  class_weight='balanced', max_depth = , min_samples_leaf = , n_estimators = , min_samples_split = , max_features = )
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# Model Precision: what percentage of positive tuples are labeled as such?
# Model Recall (sensitivity): what percentage of positive tuples are labelled as such?
print(metrics.classification_report(y_test, y_pred)) 




#plot ROC curve
probas_ = clf.fit(X_train, y_train).predict_proba(X_test)
fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1], pos_label=1)
roc_auc = auc(fpr, tpr)
#0.742530345471522
pl.clf()
pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
pl.plot([0, 1], [0, 1], 'k--')
pl.xlim([0.0, 1.0])
pl.ylim([0.0, 1.0])
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.title('Receiver operating characteristic')
pl.legend(loc="lower right")
pl.savefig('RandomForest_ROC_bayesian_AllGenes.png', dpi = 2000)

#plot pr curve
precision, recall, _  = precision_recall_curve(y_test, probas_[:, 1])
pr_auc = auc(recall, precision)
#0.7623071899295091
pl.clf()
pl.plot(recall, precision, label='Precision recall curve (area = %0.2f)' % pr_auc)
pl.plot([0, 1], [0, 1], 'k--')
pl.xlim([0.0, 1.0])
pl.ylim([0.0, 1.0])
pl.xlabel('Recall')
pl.ylabel('Precision')
pl.title('Precision recall curve')
pl.legend(loc="lower right")
pl.savefig('RandomForest_prAUC_bayesian_AllGenes.png', dpi = 2000)

