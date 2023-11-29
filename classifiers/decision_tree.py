from sklearn.tree import DecisionTreeClassifier

def classify(X_train, Y_train, X_test):
    clf = DecisionTreeClassifier()
    clf.fit(X_train, Y_train)
    return clf.predict(X_test)