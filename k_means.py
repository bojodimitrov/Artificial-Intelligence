import random
import math
import numpy as np

FILE = open("normal.txt", mode="r")

content = FILE.readlines()
dataset = []
for x in content:
    pair = x.strip().split("\t")
    dataset.append((float(pair[0]), float(pair[1])))

def calculate_cluster_points(dataset, cluster_centers):
    clusters = {}
    for data in dataset:
        optimal_centroid_distance = math.inf
        optimal_centroid = (0, 0)
        for centroid in cluster_centers:
            current_distance = np.linalg.norm(np.subtract(data, centroid))
            if(current_distance < optimal_centroid_distance):
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
    return new_clusters

print(find_centers(dataset, 4).keys())