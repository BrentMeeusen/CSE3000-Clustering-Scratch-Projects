# Reads a line from a file, removes the EOL and splits on ","
def read_line(file):
	return file.readline().rstrip("\r\n").split(",")


# Gets the variables from `names_and_scores.csv`
def get_project_data(row):
	parts = row.split(",")
	return parts[0], "".join(parts[1:-1]), parts[-1]


# Returns the found data, or the default value if no data was found
def get_data(p_id, index, default=1):

	# Get the data if possible, if not, return default value
	if(datapoints[index][0] == ''): return default

	# Setup variables
	data = datapoints[index]
	data_p_id = int(data[0])

	# Find the next closest ID to p_id
	while p_id > data_p_id:
		data = read_line(files[index])
		datapoints[index] = data
		data_p_id = int(data[0]) if data[0] != '' else p_id + 1
	
	# Return the found data, or the default if nothing was found
	return int(data[1]) if p_id == data_p_id else default



# Setup variables
include_remixes = False

# Open all files (except for the project names)
folder = ("with" if include_remixes else "without") + "_remixes\\"
filenames = ["cc", "num_blocks", "num_procedures", "num_sprites_2"]
files = list(map(lambda filename: open("data\\" + folder + filename + ".csv", encoding="utf-8"), filenames))

# Ignore the headers and read the first data points
list(map(lambda file: file.readline(), files))
datapoints = list(map(lambda file: read_line(file), files))

# Open the project names file and skip the header
names = open("data\\" + folder + "names_and_scores.csv", encoding="utf-8")
names.readline()

# Create a file for the merged data and write the headers
merged = open("data\\merged_data.csv", "w", encoding="utf-8")
merged.write("project_ID,name,dr_scratch,cc,num_blocks,num_procedures,num_sprites\n")


# Since `names.csv` contains all IDs of all projects, we have seen all projects if we've looped over the entire file. Additionally, we can make use of the fact that all `csv` files are sorted ascendingly on project ID.
# Merge the data into `merged.csv`
merged_projects = 0
for row in names:

	# Get the project's data
	p_id, name, dr_scratch_score = get_project_data(row)

	# Setup default value and array for found values
	defaults = [1, 0, 0, 0]
	found = [p_id, "\"" + name.rstrip("\r\n") + "\"", dr_scratch_score.rstrip("\r\n")]

	# Loop over all defaults and store the data
	p_id = int(p_id)
	for i, d in enumerate(defaults):
		found.append(str(get_data(p_id, i, d)))

	# Write the found data to the merge file
	merged.write(",".join(found) + "\n")
	merged_projects += 1

# Close all the files
list(map(lambda file: file.close(), files))
names.close()
merged.close()

# Print closing message
print("Finished merging " + str(merged_projects) + " projects.")
