class cycle_graph():
	"""A package built to support research into graphs for the 
	William and Mary EXTREEMS-QED program."""

	class __cg_Node():
		def __init__(self, val):
			self.prev = None
			self.next = None
			self.val = val
			self.spin = 0
			self.pos = 0
			self.n = 0

		def __gt__(self, other):
			s = self.spin - other.spin
			d = other.pos - self.pos
			if other.pos > self.pos:
				if s > d:
					return True
			if other.pos < self.pos:
				if s > d + self.n:
					return True
			return False

	def __init__(self, list_, n = 0):
		self.__base_node = None
		self.__standing = None
		self.__compare = None
		self.__length = 0
		self.__input(list_, n)

	###Initialization Functions
	def __input(self, list_, n = 0):
		for i in list_:
			self.__insert(i)
		self.__pos_assign(n)
		self.__spin_assign()
		self.__standing = self.__base_node
		self.__compare = self.__base_node

	def __insert(self, val):
		new_node = self.__cg_Node(val)
		if self.__length == 0:
			new_node.next = new_node
			new_node.prev = new_node
			self.__base_node = new_node
		else:
			self.__base_node.prev.next = new_node
			new_node.prev = self.__base_node.prev
			self.__base_node.prev = new_node
			new_node.next = self.__base_node
		self.__length = self.__length + 1
		current = self.__base_node
		for _ in range(self.__length):
			current.n = self.__length
			current = current.next

	def __pos_assign(self, n):
		current = self.__base_node
		for i in range(1, self.__length + 1):
			if i + n > self.__length:
				current.pos = i + n - self.__length
			else:
				current.pos = i + n
			current = current.next

	def __spin_assign(self):
		current = self.__base_node
		for _ in range(1, self.__length + 1):
			current.spin = current.val - current.pos
			current.n = self.__length
			current = current.next
		self.optimize()

	###Property Functions
	def __len__(self):
		return self.__length

	def __str__(self):
		if self.__length == 0:
			return ""
		current = self.__base_node
		string = ""
		for _ in range(self.__length - 1):
			string = string + str(current.val) + " "*(3 - len(str(current.val))) + "-> "
			current = current.next
		string = string + str(current.val)
		return string

	def dist_print(self):
		""" Returns a string of the spins copying the format of the str function """
		if self.__length == 0:
			return ""
		current = self.__base_node
		string = ""
		for _ in range(self.__length - 1):
			string = string + str(current.spin) + " "*(3 - len(str(current.spin))) + "-> "
			current = current.next
		string = string + str(current.spin)
		return string

	def dist_list(self):
		""" Returns a list of the spins """
		if self.__length == 0:
			return ""
		current = self.__base_node
		list_ = []
		for _ in range(self.__length - 1):
			list_.append(current.spin)
			current = current.next
		list_.append(current.spin)
		return list_

	def total_spin(self):
		""" Finds the sum of the absolute values of the spins """
		current = self.__base_node
		total = 0
		for _ in range(self.__length):
			total = total + abs(current.spin)
			current = current.next
		return total

	def terms(self):
		""" Returns the elements in the cycle in list format """
		current = self.__base_node
		out = []
		for _ in range(self.__length):
			out.append(current.val)
			current = current.next
		return out

	def not_ordered(self):
		""" Tests the ordering of the cycle and returns false if it is, and true if it is not """
		current = self.__base_node
		for _ in range(self.__length):
			if current.pos != current.val:
				return True
			current = current.next
		return False

	def __getitem__(self, key):
		if key > self.__length and key < 1:
			raise IndexError
		current = self.__base_node
		while current.pos != key:
			current = current.next
		return current.val

	def value(self, node = ''):
		""" Returns the value of the standing node by default. 
		With the argument 'comp', it returns the value of the comparison node.
		With the argument 'next', it returns the value of the next node. """
		if node == 'comp':
			return self.__compare.val
		elif node == 'next':
			return self.__standing.next.val
		return self.__standing.val

	def spin(self, node = ''):
		""" Returns the spin of the standing node by default. 
		With the argument 'comp', it returns the spin of the comparison node.
		With the argument 'next', it returns the spin of the next node. """
		if node == 'comp':
			return self.__compare.spin
		elif node == 'next':
			return self.__standing.next.spin
		return self.__standing.spin

	def position(self, node = ''):
		""" Returns the postion of the standing node by default. 
		With the argument 'comp', it returns the postion of the comparison node.comparison."""
		if node == 'comp':
			return self.__compare.pos
		return self.__standing.pos

	def compare(self, node = ''):
		if node == 'comp':
			return self.__compare > self.__standing
		return self.__standing > self.__standing.next

	###Sorting Functions
	def optimize(self):
		""" Optimizes the spins by minimizing their values """
		temp = self.dist_list()
		if sum(temp) == 0:
			while max(temp) - min(temp) > self.__length:
				max_term = max(temp) - self.__length
				min_term = min(temp) + self.__length
				temp[temp.index(max(temp))] = max_term
				temp[temp.index(min(temp))] = min_term

			current = self.__base_node
			for i in temp:
				current.spin = i
				current = current.next

	def next_node(self, node = ''):
		""" Sends the standing node to the next node by default.
		With the argument 'comp', sends the compare node to its next node."""
		if node == 'comp':
			self.__compare = self.__compare.next
			return
		self.__standing = self.__standing.next

	def prev_node(self):
		self.__standing = self.__standing.next

	def reset(self, node = ''):
		""" Sends the standing node to the base node by default.
		With the argument 'comp', sends the compare node to the base node."""
		if node == 'comp':
			self.__compare = self.__base_node
			return
		self.__standing = self.__base_node

	def send(self, key):
		""" Sends the standing node to the position key"""
		if key > self.__length and key < 1:
			raise IndexError
		while self.__standing.pos != key:
			self.__standing = self.__standing.next

	def swap(self):
		"""Swaps the standing node with the its next neighbor"""
		if self.compare():
			p_1 = self.__standing
			p_2 = self.__standing.next
			p_1.next = p_2.next
			p_2.prev = p_1.prev
			p_1.prev.next = p_2
			p_2.next.prev = p_1
			p_1.prev = p_2
			p_2.next = p_1
			if p_1 == self.__base_node:
				self.__base_node = p_2
			elif p_2 == self.__base_node:
				self.__base_node = p_1
			self.__pos_assign(0)
			self.__spin_assign()	