#from numpy import diff

class Division:
	def __init__(self, points):
		self.points = sorted(points)
		#self.norm = min(diff(self.points))
		#assert(self.norm > 0)

	def __iter__(self):
		return iter(self.points)

	def __getitem__(self, index):
		return self.points[index]

	def __add__(self, d):
		newpoints = self.points[:]
		for point in d.points:
			if point not in newpoints:
				newpoints.append(point)

		return Division(newpoints)

	def __repr__(self):
		return self.points.__repr__()

	def __eq__(self, d2):
		return self.points == d2.points

	def restrict(self, a, b):
		return Division([a] + [x for x in self.points if a < x < b] + [b])