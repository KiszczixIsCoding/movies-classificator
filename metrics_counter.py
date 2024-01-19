from sklearn.metrics import confusion_matrix
import numpy as np

def count_confusion_matrix(y_true, y_pred):
    # Compute the confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # Print the confusion matrix in text format
    print("Confusion Matrix:")
    for i in range(len(cm)):
        print("True Class", i, cm[i])

    main_diagonal = cm.diagonal()
    secondary_diagonal = cm[:, ::-1].diagonal()

    # Calculate accuracy for each diagonal
    accuracy_main_diagonal = sum(main_diagonal) / sum(sum(cm))
    accuracy_secondary_diagonal = sum(secondary_diagonal) / sum(sum(cm))

    # Print accuracy for each diagonal
    print("Accuracy for Main Diagonal:", accuracy_main_diagonal)
    print("Accuracy for Secondary Diagonal:", accuracy_secondary_diagonal)