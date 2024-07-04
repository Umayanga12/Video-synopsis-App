import numpy as np
from sklearn.cluster import DBSCAN

# Assuming you have a list of object features (e.g., position, size, motion vectors)
object_features = np.array([...])  # Replace with your actual feature list

# Apply DBSCAN clustering
clustering = DBSCAN(eps=3, min_samples=2).fit(object_features)

# Group events based on clusters
clusters = {}
for idx, label in enumerate(clustering.labels_):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(active_periods[idx])
