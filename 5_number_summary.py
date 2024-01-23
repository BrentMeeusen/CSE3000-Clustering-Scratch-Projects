import statistics

# Returns the median of the given array
def compute_median(data):
	median_index = int(len(data) / 2)
	return (data[median_index - 1] + data[median_index]) / 2 if len(data) % 2 == 0 else data[median_index]


# Computes and returns the 5-number summary, the mean, and the mode for the given index
def five_number_summary(data, index):
	
	# Flatten and sort the list
	data = sorted(list(map(lambda v: v[index], data)))
	size = len(data)

	# Find the min, Q1, median, Q3, max
	smallest = data[0]
	q1 = compute_median(data[:int(size / 2)])
	median = compute_median(data)
	q3 = compute_median(data[(int(size / 2) + (0 if size % 2 == 0 else 1)):])
	largest = data[-1]

	# Calculate the mean
	mean = statistics.mean(data)
	mode = statistics.multimode(data)

	# Return the 5 number summary
	return [smallest, q1, median, q3, largest, mean, mode]



# Setup main array
data = []

# Open file and ignore the headers
file = open("data\\merged_data.csv", encoding="utf-8")
file.readline()

# Read all lines and parse to create an array of arrays with integer values
for line in file:
	p_id, rest = line.rstrip("\r\n").split(",", 1)
	rest = rest.split("\",")[-1].split(",")
	data.append(list(map(lambda v: int(v), rest)))

# Setup output file
summaries = open("data\\5_number_summaries\\new_summary.csv", "w", encoding="utf-8")
summaries.write("value,min,q1,median,q3,max,mean,mode\n")

# Generate the 5-number summaries and write them to the output file
for i, v in enumerate(["dr_scratch", "cc", "num_blocks", "num_procedures", "num_sprites"]):
	summary = five_number_summary(data, i)
	summary[6] = ";".join(list(map(lambda v: str(v), summary[6])))
	summary = list(map(lambda v: str(v), summary))
	summaries.write(v + "," + ",".join(summary) + "\n")

# Close all the files
file.close()
summaries.close()

# Print closing message
print("Finished generating 5-number summaries for `merged_data.csv`.")
