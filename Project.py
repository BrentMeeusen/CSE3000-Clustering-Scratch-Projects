class Project:

	def __init__(self, row):
		self.parse_row(row)


	def parse_row(self, row):
		self.p_id, rest = row.rstrip("\r\n").split(",", 1)
		parts = rest.split("\",")
		self.name = "\",".join(parts[:-1])[1:]
		self.dr_scratch, self.cc, self.num_blocks, self.num_procedures, self.num_sprites = list(map(lambda p: int(p), parts[-1].split(",")))

		self.blocks_per_procedure = self.num_blocks / self.num_procedures if self.num_procedures > 0 else self.num_procedures
		self.blocks_per_sprite = self.num_blocks / self.num_sprites if self.num_sprites > 0 else self.num_sprites


	def get_columns(self, columns):
		values = []
		for col in columns: values.append(getattr(self, col))
		return values


	def __repr__(self):
		attributes = list(map(lambda a: str(a), [self.p_id, hasattr(self, "name_vector"), self.dr_scratch, self.cc, self.num_blocks, self.num_procedures, self.num_sprites, self.blocks_per_procedure, self.blocks_per_sprite]))
		attributes.insert(1, self.name)
		return ";".join(attributes)
