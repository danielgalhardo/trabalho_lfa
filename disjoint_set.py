class DisjointSet(object):

	def __init__(self,itens):

		self._disjoint_set = list()

		if itens:
			for item in set(itens):
				self._disjoint_set.append([item])

	def _indice(self,item):
		for s in self._disjoint_set:
			for _item in s:
				if _item == item:
					return self._disjoint_set.index(s)
		return None

	def find(self,item):
		for n in self._disjoint_set:
			if item in n:
				return n
		return None

	def find_set(self,item):

		n = self._indice(item)

		return n+1 if n is not None else None

	def union(self,item1,item2):
		a = self._indice(item1)
		b = self._indice(item2)

		if a != b:
			self._disjoint_set[a] += self._disjoint_set[b]
			del self._disjoint_set[b]
	
	def get(self):
		return self._disjoint_set