from sklearn.ensemble import RandomForestClassifier

def classify(X_train, Y_train, X_test):
    clf = RandomForestClassifier()
    clf.fit(X_train, Y_train)
    return clf.predict(X_test)