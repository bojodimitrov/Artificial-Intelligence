import random
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

FILE = open("data/normal.txt", mode="r")

content = FILE.readlines()
DATASET = []
for x in content:
    pair = x.strip().split("\t")
    DATASET.append((float(pair[0]), float(pair[1])))

def plot_dict(dict):
    for key, value in dict.items():
        plt.scatter([i[0] for i in value], [i[1] for i in value])
        plt.scatter(key[0], key[1], marker="*")
    plt.show()

def calculate_cluster_points(dataset, cluster_centers):
    clusters = {}
    for data in dataset:
        optimal_centroid_distance = math.inf
        optimal_centroid = (0, 0)
        for centroid in cluster_centers:
            current_distance = math.hypot(centroid[0] - data[0], centroid[1] - data[1])
            if current_distance <= optimal_centroid_distance:
                optimal_centroid_distance = current_distance
                optimal_centroid = centroid
        try:
            clusters[optimal_centroid].append(data)
        except KeyError:
            clusters[optimal_centroid] = [data]
    
    return clusters

def converged(cluster_centers, next_cluster_centers):
    return set(cluster_centers) == set(next_cluster_centers)

def reevaluate_centers(cluster_centers, clusters):
    new_cluster_centers = []
    cluster_points = sorted(clusters.keys())
    for point in cluster_points:
        new_center = np.mean(clusters[point], axis=0)
        new_cluster_centers.append((new_center[0], new_center[1]))
    return new_cluster_centers

def find_centers(dataset, number_of_clusters):
    cluster_centers = random.sample(dataset, number_of_clusters)
    next_cluster_centers = random.sample(dataset, number_of_clusters)
    while np.array_equal(cluster_centers, next_cluster_centers):
        next_cluster_centers = random.sample(dataset, number_of_clusters)
    new_clusters = None
    while not converged(cluster_centers, next_cluster_centers):
        cluster_centers = next_cluster_centers
        new_clusters = calculate_cluster_points(dataset, next_cluster_centers)
        next_cluster_centers = reevaluate_centers(cluster_centers, new_clusters)
        plot_dict(new_clusters)
    return new_clusters

plt.scatter([i[0] for i in DATASET], [i[1] for i in DATASET])
plt.show()

RESULT = find_centers(DATASET, 4)
plot_dict(RESULT)

plt.show()
