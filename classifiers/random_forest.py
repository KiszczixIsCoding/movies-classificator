from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


def forest_classify(X_train, Y_train, X_test):
    clf = RandomForestClassifier()
    print(len(X_train))
    print(len(Y_train.reshape(-1, 1)))
    print(Y_train.ravel().shape)

    clf.fit(X_train, Y_train.ravel())
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

    return int(clf.predict(X_test.reshape(1, -1))[0])