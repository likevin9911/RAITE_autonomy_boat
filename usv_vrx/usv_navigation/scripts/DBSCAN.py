import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

# Load data from the CSV file
data = []
with open('gps_coordinates.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        latitude = float(row[0])
        longitude = float(row[1])
        data.append([latitude, longitude])

data = np.array(data)

# Apply DBSCAN for clustering
dbscan = DBSCAN(eps=0.0000002, min_samples=5).fit(data)
labels = dbscan.labels_

# Plot the clustered data
plt.figure(figsize=(8, 6))
unique_labels = set(labels)
colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = data[class_member_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('DBSCAN Clustering of GPS Coordinates')
plt.xlabel('latitude')
plt.ylabel('longitude')
plt.show()
