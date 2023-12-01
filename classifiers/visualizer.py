import matplotlib.pyplot as plt

# Plot the decision tree
from sklearn.tree import plot_tree


def draw_tree(clf):
  plt.figure(figsize=(20, 12))
  plot_tree(clf, filled=True, class_names=['0', '1', '2', '3', '4', '5'], rounded=True, fontsize=10)
  plt.show()