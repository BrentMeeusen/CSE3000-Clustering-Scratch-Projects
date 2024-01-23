class ClusterProperties:
	def __init__(self, cluster_id):
		self.cluster_id = cluster_id
		self.projects = []

		self.min_dr_scratch = float("inf")
		self.max_dr_scratch = float("-inf")
		self.min_cc = float("inf")
		self.max_cc = float("-inf")
		self.min_blocks = float("inf")
		self.max_blocks = float("-inf")
		self.min_procedures = float("inf")
		self.max_procedures = float("-inf")
		self.min_sprites = float("inf")
		self.max_sprites = float("-inf")


	def add(self, project):
		self.projects.append(project)
		self.update_dr_scratch(project.dr_scratch)
		self.update_cc(project.cc)
		self.update_blocks(project.num_blocks)
		self.update_procedures(project.num_procedures)
		self.update_sprites(project.num_sprites)


	def update_dr_scratch(self, v):
		self.min_dr_scratch = min(self.min_dr_scratch, v)
		self.max_dr_scratch = max(self.max_dr_scratch, v)

	def update_cc(self, v):
		self.min_cc = min(self.min_cc, v)
		self.max_cc = max(self.max_cc, v)

	def update_blocks(self, v):
		self.min_blocks = min(self.min_blocks, v)
		self.max_blocks = max(self.max_blocks, v)

	def update_procedures(self, v):
		self.min_procedures = min(self.min_procedures, v)
		self.max_procedures = max(self.max_procedures, v)

	def update_sprites(self, v):
		self.min_sprites = min(self.min_sprites, v)
		self.max_sprites = max(self.max_sprites, v)


	def to_dict(self):
		return {
			"Cluster ID": self.cluster_id,
			"Cluster size": len(self.projects),
			"Min Dr Scratch": self.min_dr_scratch,
			"Max Dr Scratch": self.max_dr_scratch,
			"Min CC": self.min_cc,
			"Max CC": self.max_cc,
			"Min blocks": self.min_blocks,
			"Max blocks": self.max_blocks,
			"Min procedures": self.min_procedures,
			"Max procedures": self.max_procedures,
			"Min sprites": self.min_sprites,
			"Max sprites": self.max_sprites
		}
