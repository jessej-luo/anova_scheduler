class Edge(object):
	def __init__(self, u, v, w):
		self.source = u
		self.sink = v
		self.capacity = w

	def __repr__(self):
		return "%s->%s" % (self.source, self.sink)

class FlowNetwork(object):
	def __init__(self):
		self.adj = {}
		self.flow = {}

	def add_vertex(self, vertex):
		self.adj[vertex] = []

	def get_edges(self, v):
		return self.adj[v]

	def add_edge(self, u, v, w=0):
		if u == v:
			raise ValueError("u == v")
		edge = Edge(u, v, w)
		redge = Edge(v, u, 0)
		edge.redge = redge
		redge.redge = edge
		self.adj[u].append(edge)
		self.adj[v].append(redge)
		self.flow[edge] = 0
		self.flow[redge] = 0

	def find_path(self, source, sink, path):
		if source == sink:
			return path
		for edge in self.get_edges(source):
			residual = edge.capacity - self.flow[edge]
			if residual > 0 and edge not in path:
				result = self.find_path(edge.sink, sink, path + [edge])
				if result != None:
					return result

	def max_flow(self, source, sink, schools):
		path = self.find_path(source, sink, [])
		while path != None:
			residuals = [edge.capacity - self.flow[edge] for edge in path]
			flow = min(residuals)
			for edge in path:
				self.flow[edge] += flow
				self.flow[edge.redge] -= flow
			path = self.find_path(source, sink, [])
		#iterate over all schools and check for -1
		matching = {}
		for school in schools:
			for edge in self.get_edges(school):
				if self.flow[edge] == -1:
					if edge.source not in matching:
						matching[edge.source] = [edge.sink]
					else:
						matching[edge.source].append(edge.sink)
					
		max_flow = sum(self.flow[edge] for edge in self.get_edges(source))
		if max_flow == len(self.get_edges(source)):
			print("Max Match found")
			return matching
		else:
			return "No Max Matching Found"