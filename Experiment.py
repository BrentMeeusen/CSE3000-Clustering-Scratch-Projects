from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt

from ClusterProperties import ClusterProperties


class Experiment:

	def __init__(self, name, data, normalised_data, vectorised_names, eps_set, min_samples_set):
		self.name = name
		self.data = data
		self.normalised_data = normalised_data
		self.vectorised_names = vectorised_names
		self.eps_set = eps_set
		self.min_samples_set = min_samples_set


	def concat(self, a, b):
		return np.concatenate((a, b), axis=1)

	def get_values(self, projects, columns):
		data = list(map(lambda p: p.get_columns(columns), projects))
		return np.matrix(data) if len(columns) != 1 else np.vstack(data)


	def generate_and_save_pca(self, projects, location):
		pca = PCA(n_components=2)
		res = pca.fit_transform(projects)

		fig, ax = plt.subplots()
		ax.scatter(res[:, 0], res[:, 1])
		plt.title("PCA of " + str(len(projects)) + " datapoints with " + str(len(projects[0])) + " dimensions")
		plt.xlabel("Principal Component 1")
		plt.ylabel("Principal Component 2")
		fig.savefig("figures/" + location + "/PCA.png")


	def generate_dataset(self, projects):
		matrix = np.empty((len(projects), 0), dtype=float)
		if self.data:
			matrix = self.concat(matrix, self.get_values(projects, ["cc", "num_blocks", "num_procedures", "num_sprites"]))
		if self.normalised_data:
			matrix = self.concat(matrix, self.get_values(projects, ["blocks_per_procedure", "blocks_per_sprite"]))
		if self.vectorised_names:
			matrix = self.concat(matrix, self.get_values(projects, ["name_vector"]))

		return matrix


	def find_clusters(self, projects):

		# Setup parameters to collect the clusters
		self.clusters = []
		collected = sorted(list(zip(projects, self.algorithm.labels_)), key=lambda x: x[1])
		current = -1
		cluster = ClusterProperties(current)

		# Put all points in the clusters they belong to
		for point in collected:
			if point[1] != current:
				current += 1
				self.clusters.append(cluster)
				cluster = ClusterProperties(current)

			cluster.add(point[0])
		self.clusters.append(cluster)


	def compute_silhouette_scores(self, projects, labels):

		# If there's 0 or 1 clusters, or same number of labels as there are projects, silhouette score is undefined
		if max(labels) <= 0 or max(labels) >= len(projects) - 2:
			self.silhouette_score_with_outliers = -99
			self.silhouette_score_without_outliers = -99
			return

		# Compute silhouette score with all projects
		self.silhouette_score_with_outliers = silhouette_score(projects, labels)

		# Exclude outliers, then compute silhouette score
		zipped = list(zip(projects, labels))
		zipped = list(filter(lambda z: z[1] >= 0, zipped))
		projects, labels = list(zip(*zipped))
		self.silhouette_score_without_outliers = silhouette_score(projects, labels)


	def save_results(self, eps, min_samples, folder):
		file = open(folder + "/eps" + str(eps) + ", min_samples" + str(min_samples) + ".txt", "w", encoding="utf-8")
		file.write("eps:         " + str(eps) + "\n")
		file.write("min_samples: " + str(min_samples) + "\n")
		file.write("Silhouette score including outliers: " + str(self.silhouette_score_with_outliers) + "\n")
		file.write("Silhouette score excluding outliers: " + str(self.silhouette_score_without_outliers) + "\n\n")
		file.write(tabulate(list(map(lambda cp: cp.to_dict().values(), self.clusters)), headers=self.clusters[0].to_dict().keys()))
		file.close()


	def run(self, projects, dataset, eps, min_samples, folder):
		self.algorithm = DBSCAN(eps=eps, min_samples=min_samples)
		self.algorithm.fit(dataset)

		self.find_clusters(projects)
		self.compute_silhouette_scores(dataset, self.algorithm.labels_)
		self.save_results(eps, min_samples, "results/" + folder)


	def run_all(self, projects, folder):
		dataset = np.asarray(self.generate_dataset(projects))
		self.generate_and_save_pca(dataset, folder)

		num_items = len(self.eps_set) * len(self.min_samples_set)
		num_finished = 0

		for eps in self.eps_set:
			for min_samples in self.min_samples_set:
				print("  eps=" + str(eps) + ", min_samples=" + str(min_samples) + "; Clustering...")
				self.run(projects, dataset, eps, min_samples, folder)
				num_finished += 1

				print("  {:.2f}".format(float(num_finished / num_items) * 100) + "% done.")
