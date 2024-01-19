from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

from classifiers.visualizer import draw_tree

def tree_classify(X_train, Y_train, X_test):
    clf = DecisionTreeClassifier(max_depth=3, max_features='sqrt')
    print(len(X_train))
    print(len(Y_train.reshape(-1, 1)))
    print(Y_train.reshape(-1, 1).shape)

    clf.fit(X_train, Y_train.reshape(-1, 1))
    #
    # param_grid = {
    #     'max_depth': [3, 5, 7, None],
    #     'min_samples_split': [2, 5, 10],
    #     'min_samples_leaf': [1, 2, 4],
    #     'max_features': ['auto', 'sqrt', 'log2', None]
    # }

    # # Instantiate the grid search
    # grid_search = GridSearchCV(clf, param_grid, cv=5, scoring='accuracy')
    #
    # # Fit the grid search to the data
    # grid_search.fit(X_train, Y_train.reshape(-1, 1))
    #
    # # Get the best parameters and best estimator
    # best_params = grid_search.best_params_
    # best_estimator = grid_search.best_estimator_
    # best_accuracy = grid_search.best_score_
    #
    # print("Best Parameters:", best_params)
    # print("Best Estimator:", best_estimator)
    # print("Best Accuracy:", best_accuracy)
    #
    # draw_tree(clf)
    return int(clf.predict(X_test.reshape(1, -1))[0])