"""
Implementation of kMeans algorithm
"""
import random
import math
import sys
import numpy as np
import matplotlib.pyplot as plt

PATH_TO_FILE = sys.argv[1]
NUMBER_OF_CLUSTERS = sys.argv[2]

def read_data(filename):
    """
    Reads pairs of numbers from file and creates array of tupples
    File: xx.xxx yy.yyy -> [(xx.xxx, yy.yyy)]
    """
    file = open(filename, mode="r")
    content = file.readlines()
    dataset = []
    for line in content:
        pair = line.strip().split("\t")
        dataset.append((float(pair[0]), float(pair[1])))
    return dataset

def plot_dict(dictionary):
    """
    Plots dictionary, containing centers with corresponding points in cluster
    """
    for key, value in dictionary.items():
        plt.scatter([i[0] for i in value], [i[1] for i in value])
    for key in dictionary.keys():
        plt.scatter(key[0], key[1], marker="*")

def calculate_cluster_points(dataset, cluster_centers):
    """
    Assigns points to closest cluster center
    """
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
    """
    Checks if the iterations has converged
    """
    return set(cluster_centers) == set(next_cluster_centers)

def reevaluate_centers(clusters):
    """
    Moves the center of a cluster closer to its geometrical center
    """
    new_cluster_centers = []
    cluster_points = sorted(clusters.keys())
    for point in cluster_points:
        new_center = np.mean(clusters[point], axis=0)
        new_cluster_centers.append((new_center[0], new_center[1]))
    return new_cluster_centers

def find_centers(dataset, number_of_clusters):
    """
    The core of the algorithm
    """
    cluster_centers = random.sample(dataset, number_of_clusters)
    next_cluster_centers = random.sample(dataset, number_of_clusters)
    while np.array_equal(cluster_centers, next_cluster_centers):
        next_cluster_centers = random.sample(dataset, number_of_clusters)
    new_clusters = None
    while not converged(cluster_centers, next_cluster_centers):
        cluster_centers = next_cluster_centers
        new_clusters = calculate_cluster_points(dataset, next_cluster_centers)
        next_cluster_centers = reevaluate_centers(new_clusters)
    return new_clusters

DATASET = read_data(PATH_TO_FILE)

plt.scatter([i[0] for i in DATASET], [i[1] for i in DATASET])
#plt.savefig("normal_scattered.png")

RESULT = find_centers(DATASET, 4)
plot_dict(RESULT)

plt.savefig("clustered.png")
