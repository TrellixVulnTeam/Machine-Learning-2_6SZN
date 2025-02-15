print("hello world");
# Homework 2
import numpy as np
from sklearn import datasets
from sklearn.metrics import accuracy_score # other metrics too pls!
from sklearn.ensemble import RandomForestClassifier 
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier# more!
from sklearn.model_selection import KFold
from sklearn.model_selection import ParameterGrid
import matplotlib.pyplot as plt
import itertools as it
import json
import re

# adapt this code below to run your analysis
# 1. Write a function to take a list or dictionary of clfs and hypers(i.e. use logistic regression), each with 3 different sets of hyper parameters for each
# 2. Expand to include larger number of classifiers and hyperparameter settings
# 3. Find some simple data
# 4. generate matplotlib plots that will assist in identifying the optimal clf and parampters settings
# 5. Please set up your code to be run and save the results to the directory that its executed from
# 6. Investigate grid search function

M = np.array([[1,2],[3,4],[4,5],[4,5],[4,5],[4,5],[4,5],[4,5]])
L = np.ones(M.shape[0])
n_folds = 5

data = (M, L, n_folds)

def run(a_clf, data, clf_hyper={}):
  M, L, n_folds = data # unpack data container
  kf = KFold(n_splits=n_folds) # Establish the cross validation
  ret = {} # classic explication of results

  for ids, (train_index, test_index) in enumerate(kf.split(M, L)):
    clf = a_clf(**clf_hyper) # unpack parameters into clf is they exist
    clf.fit(M[train_index], L[train_index])
    pred = clf.predict(M[test_index])
    ret[ids]= {'clf': clf,
               'train_index': train_index,
               'test_index': test_index,
               'accuracy': accuracy_score(L[test_index], pred)}
  return ret

results = run(RandomForestClassifier, data, clf_hyper={})
#LongLongLiveGridS#LongLon#LLongLiveGridSearch!gLiveGridSearch!
###################################################################

models_dict = {
    "neighbor": KNeighborsClassifier,
    "regression": LogisticRegression,
    "RandomForestClassifier": RandomForestClassifier,
}

#The  three different models imputs
inputs = {
    'neighbor': {
        #'model': KNeighborsClassifier(),
        
            'n_neighbors' : [3,4,5,6,7,8],
            "weights":["uniform", "distance"],
            'algorithm': ['ball_tree','auto',"kd_tree"]
            
        
    },
    'regression': {
        #'model': LogisticRegression(),
       
            "penalty":[ "l2", "none"]
        
    },
     'RandomForestClassifier': {
        #'model': RandomForestClassifier(),
        "n_estimators": [100, 200, 500, 1000],
        "max_features": ["auto", "sqrt", "log2"],
        "bootstrap": [True],
        "criterion": ["gini", "entropy"],
        "oob_score": [True, False],
            
        
    }
    
}
################################################################
# Add the run method with data set
#Add the dataset in 

Irisdataset = datasets.load_iris()
M = Irisdataset.data
L = Irisdataset.target
n_folds = 5

data = (M, L, n_folds)

def run(a_clf, data, clf_hyper={}):
  M, L, n_folds = data # unpack data container
  kf = KFold(n_splits=n_folds) # Establish the cross validation
  ret = {} # classic explication of results

  for ids, (train_index, test_index) in enumerate(kf.split(M, L)):
    clf = a_clf(**clf_hyper) # unpack parameters into clf is they exist
    clf.fit(M[train_index], L[train_index])
    pred = clf.predict(M[test_index])
    ret[ids]= {'clf': clf,
               'train_index': train_index,
               'test_index': test_index,
               'accuracy': accuracy_score(L[test_index], pred)}
  return ret

#model = KNeighborsClassifier()
#parameters = {'n_neighbors' : 3, 'algorithms': 'auto'}
#model.set_params(**parameters)

#model.set_params(n_neightbors=3, algorithms='auto')

# inputs 
# list of models
# list of hyperparameters

# %%
# ╔═════════════════════════╗
#   Define: build_clf_acc_dict
# ╚═════════════════════════╝


def build_clf_acc_dict(results_dict):
    clf_accuracy_dict = {}

    for key in results_dict:
        k1 = results_dict[key]["clf"]
        v1 = results_dict[key]["accuracy"]
        k1Test = str(k1)

        # Remove extra spaces in 'k1Test'
        k1Test = re.sub("\s\s+", " ", k1Test)

        # If 'k1Test' exists as a key in the clf_accuracy_dict, then append the
        # values, otherwise create a new key with a new value (v1).
        if k1Test in clf_accuracy_dict:
            clf_accuracy_dict[k1Test].append(v1)
        else:
            clf_accuracy_dict[k1Test] = [v1]

    return clf_accuracy_dict
# %%
# ╔══════════════════════╗
#   Define: plot_parameters
# ╚══════════════════════╝


def plot_parameters(clf_accuracy_dict, filename="clf_Histograms_"):

    filename_prefix = filename

    # Initialize the plot_num counter for incrementing in the loop below
    plot_num = 1

    # Adjust matplotlib subplots for easy terminal window viewing
    left = 0.125
    right = 0.9
    bottom = 0.1
    top = 0.6
    wspace = 0.2
    hspace = 0.2

    # Determine the maximum number of K-folds for the y-axes
    n = max(len(v1) for k1, v1 in clf_accuracy_dict.items())

    # Create the plots
    for k1, v1 in clf_accuracy_dict.items():

        # For each key in our clf_accuracy_dict, create a new histogram with a given key's values
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(
            1, 1, 1
        )  # As the ax subplot numbers increase here, the plot gets smaller
        plt.hist(v1, facecolor="lightblue")
        ax.set_title(k1, fontsize=25, wrap=True)
        ax.set_xlabel("Classifer Accuracy (By K-Fold)", fontsize=15)
        ax.set_ylabel("Frequency", fontsize=15)
        # Accuracy is represented on a 0 to 1 scale (e.g. 0 or 100%)
        ax.xaxis.set_ticks(np.arange(0, 1.1, 0.1))
        ax.yaxis.set_ticks(np.arange(0, n + 1, 1))  # n represents the number of k-folds
        ax.xaxis.set_tick_params(labelsize=10)
        ax.yaxis.set_tick_params(labelsize=10)
        # Pass in the subplot adjustments from above
        plt.subplots_adjust(
            left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace
        )
        plot_num_str = str(plot_num)
        filename = filename_prefix + plot_num_str
        plt.savefig(filename, bbox_inches="tight")
        plot_num = plot_num + 1
    plt.show()
# %%
# ╔══════════════════════╗
#   Define: run_grid_search
# ╚══════════════════════╝


def run_grid_search(models_dict, hyperparameter_dict, data, filename=""):
    # Define empty dictionaries to start
    np_results = {}
    gs_accuracy = {}

    # Iterate through the model dictionary to execute each model
    for key, value in models_dict.items():

        print("Processing Model: ", key)

        # Get the hyperparameter dictionary listings for the specific model
        paramDict = hyperparameter_dict[key]

        # Use iterpools' product function to build out all possible
        # hyperparameter permutations
        keys1, values1 = zip(*paramDict.items())
        hyper_list = [dict(zip(keys1, v)) for v in it.product(*values1)]

        # Iterate through each permutation from hyper_list and add the results
        # to np_results
        for dic in hyper_list:
            np_results.update(run(value, data, dic))

        # Get the best combination of models and hyperparameters for printing
        gs_accuracy.update(build_clf_acc_dict(np_results))

        # Save the results of gs_accuracy as a JSON file
        with open("gs_accuracy.json", "w") as fp:
            json.dump(gs_accuracy, fp, sort_keys=True, indent=4)

    # Plot the parameters
    plot_parameters(gs_accuracy, filename)
    # %%
# ╔═══════════════╗
#   Run grid_search
# ╚═══════════════╝

run_grid_search(models_dict, inputs, data, "MF_clf_Histograms_")
