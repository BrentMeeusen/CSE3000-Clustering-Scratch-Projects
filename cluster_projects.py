# Import the necessary libraries
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer

from matplotlib import colormaps
import matplotlib.pyplot as plt
import numpy as np
import os, re
from datetime import datetime

from ClusterProperties import ClusterProperties
from Experiment import Experiment
from Project import Project


# Setup parameters for filtering projects
min_dr_scratch = 16			# Min Dr Scratch score to be clustered
max_samples	= 50_000		# Max number of samples to cluster

# Setup experiments
eps = np.arange(8.0, 10.1, 0.5)
min_samples = np.arange(10, 21, 5)

# Look for best fitting hyperparameters
experiments = [
	Experiment("Data only", True, False, False, np.arange(0.5, 10.1, 0.5), np.arange(5, 61, 5)),
	Experiment("Names only", False, False, True, np.arange(0.5, 10.1, 0.5), np.arange(5, 61, 5))
]

# The experiments to run
# NOTE: This overrides the `experiments` array to find the best fitting hyperparameters
experiments = [
	Experiment("Data only", True, False, False, eps, min_samples),
	Experiment("Normalised only", False, True, False, eps, min_samples),
	# Experiment("Names only", False, False, True, eps, min_samples),
	Experiment("Data and normalised", True, True, False, eps, min_samples),
	Experiment("Data and names", True, False, True, eps, min_samples),
	Experiment("All", True, True, True, eps, min_samples)
]


def format_time(diff):
	minutes = int(diff.seconds / 60)
	milliseconds = int(diff.microseconds / 1000)
	return str(minutes) + "m " + "{:.3f}".format((diff.seconds % 60) + (milliseconds / 1000)) + "s"


def read_data():
	projects = []
	file = open("data\\merged_data.csv", encoding="utf-8")
	file.readline()
	for line in file:
		projects.append(Project(line))
	return projects


def vectorise_project_names(projects):

	# Remove special characters (`?!()[]`) and collapse (multiple) whitespaces and dashes into one whitespace
	names = list(map(lambda p: re.sub("[\?!\(\)\[\]]", "", re.sub("[\s-]+", " ", p.name)), projects))

	# Vectorise the names
	alg = CountVectorizer()
	result = alg.fit_transform(names).toarray()

	# Add the name vectors to projects
	for i, p in enumerate(projects):
		p.name_vector = result[i]


# Show histogram of Dr. Scratch scores
def dr_scratch_scores_histogram(projects):
	scores = list(map(lambda p: p.dr_scratch, projects))
	fig, ax = plt.subplots()
	ax.hist(scores, range(min(scores), 23), align='left')
	ax.set_xticks(range(min(scores), 22))

	plt.title("Dr. Scratch scores distribution")
	plt.xlabel("Dr. Scratch score")
	plt.ylabel("Number of projects")
	fig.savefig("figures/histogram_dr_scratch_" + str(min(scores)) + ".png")	# Uncomment this line to generate the histograms



def main():

	main_start = datetime.now()

	print("Reading and parsing projects...")
	projects = read_data()
	dr_scratch_scores_histogram(projects)

	print("Filtering projects...")
	projects = list(filter(lambda p: p.dr_scratch >= min_dr_scratch, projects))
	print(str(len(projects)) + " projects found.")
	dr_scratch_scores_histogram(projects)

	# Exit if there are too many projects
	if len(projects) > max_samples:
		print("Error: too many projects. Limit is " + str(max_samples) + " projects. Exiting.")
		exit()

	# Vectorise project names
	vectorise_project_names(projects)

	# Setup directory to save the results
	root_folder = datetime.now().strftime("%Y%m%d %H.%M.%S")
	os.mkdir("results/" + root_folder)
	os.mkdir("figures/" + root_folder)

	# Run and save the experiments
	print("")
	for i, experiment in enumerate(experiments):
		print("Performing experiment " + str(i + 1) + " of " + str(len(experiments)) + ", \"" + experiment.name + "\"...")
		folder = "/".join([root_folder, experiment.name])
		os.mkdir("results/" + folder)
		os.mkdir("figures/" + folder)

		# Setup timer to calculate time needed for each experiment
		start = datetime.now()
		experiment.run_all(projects, folder)

		# Experiment done
		print("Experiment " + str(i + 1) + " completed in " + format_time(datetime.now() - start) + ".\r\n")

	# Program done
	print("Program completed in " + format_time(datetime.now() - main_start) + ".")



if __name__ == "__main__":
	main()
