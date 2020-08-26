# Deliverr Recruitement Exercise
# Submitted By:
# Akanksha Dara
# Stony Brook University
# akankshadara7@gmail.com

import unittest

class InventoryAllocator:
	# order - a map of items that are being ordered and how many of them are ordered.
	# warehouses - a list of object with warehouse name and inventory amounts ( pre-sorted based on cost.)
	def __init__(self):
		pass

	def allocate(self, order, warehouses):
		ret = {}
		# first pass - greedy approach
		# allocate warehouses to items that can be completely shipped from one warehouse
		for item,count in order.items():
			for warehouse in warehouses:
				if item in warehouse['inventory'] and order[item] > 0 and count <= warehouse['inventory'][item]:
					warehouse['inventory'][item] -= count
					if(warehouse['inventory'][item] == 0):
						warehouse['inventory'].pop(item)
					if warehouse['name'] not in ret:
						ret[warehouse['name']] = {item: count}
					else:
						ret[warehouse['name']][item] = count
					order[item] = 0
		
		# using list comprehension to remove items whose orders have been fulfilled without splitting the order
		order = {item:count for item,count in order.items() if count!=0}

		# second pass 
		# greedy approach
		# as asked in the question: 
		# We can assume that shipping out of one warehouse is cheaper than shipping from multiple warehouses.
		for item,count in order.items():
			num_allocated = 0
			allocations = []
			for warehouse in warehouses:
				if item in warehouse['inventory'] and num_allocated<count:
					if(num_allocated + warehouse['inventory'][item] > count):
						allocations.append({warehouse['name']: {item:count - num_allocated}})
						num_allocated += count - num_allocated
					else:
						allocations.append({warehouse['name']: {item:warehouse['inventory'][item]}})
						num_allocated += warehouse['inventory'][item]
			if(num_allocated==count):
				for allocation in allocations:
					warehouse_name = list(allocation.keys())[0]
					allocated_items = list(allocation.values())[0]
					if warehouse_name not in ret:
						ret[warehouse_name] = allocated_items
					else:
						item = list(allocated_items.items())[0]
						ret[warehouse_name][item[0]] = item[1] 

		result = [{a: ret[a]} for a in ret]
		print(result)
		return result


class TestInventoryAllocator(unittest.TestCase):
	
	def setUp(self):
		self.inventoryAllocator = InventoryAllocator()

	def test_case1(self):
		# Example given in the Question
		order = {'apple': 5, 'banana': 5, 'orange': 15}
		warehouses  = [{'name': 'owd', 'inventory': { 'apple': 5, 'orange': 10 }}, { 'name': 'dm', 'inventory': { 'banana': 5, 'orange': 10 } } ]
		output = self.inventoryAllocator.allocate(order, warehouses)
		expected = [{'owd': {'apple': 5, 'orange': 10}}, {'dm': {'banana': 5, 'orange': 5}}]
		self.assertEqual(output, expected)
		# print("Test case 1 successful")

	def test_case2(self):
		# One item is completely allocated from one warehouse, the second one is split between two
		order = {'apple': 5, 'orange':12}
		warehouses  = [{'name': 'owd', 'inventory': { 'apple': 5, 'orange': 10 }}, { 'name': 'dm', 'inventory': { 'banana': 5, 'orange': 10 } } ]
		output = self.inventoryAllocator.allocate(order, warehouses)
		expected = [{'owd': {'apple': 5, 'orange': 10}}, {'dm': {'orange': 2}}]
		self.assertEqual(output, expected)

	def test_case3(self):
		# Order can be shipped using one warehouse
		order = {'apple': 1}
		warehouses = [{'name': 'owd', 'inventory': { 'apple': 1 } }]
		output = self.inventoryAllocator.allocate(order, warehouses)
		expected = [{'owd': {'apple': 1}}]
		self.assertEqual(output, expected)

	def test_case4(self):
		# Order cannot be shipped because there is not enough inventory
		order = {'apple': 1}
		warehouses = [{'name': 'owd', 'inventory': { 'apple': 0 } }]
		output = self.inventoryAllocator.allocate(order, warehouses)
		expected = []
		self.assertEqual(output, expected)

	def test_case5(self):
		# One item is completely allocated from one warehouse, the second one is completely allocated from another warehouse
		order = {'apple':3, 'orange':12}
		warehouses  = [{'name': 'w1', 'inventory': { 'apple': 5, 'orange': 4 }}, { 'name': 'w2', 'inventory': { 'banana': 5, 'orange': 4 }},{ 'name': 'w3', 'inventory': { 'orange': 40 }} ]
		output = self.inventoryAllocator.allocate(order, warehouses)
		expected = [{'w1': {'apple': 3}}, {'w3': {'orange': 12}}]
		self.assertEqual(output, expected)

	def test_case5(self):
		# One item is completely allocated from one warehouse, the second one is split between 3 warehouses
		order = {'apple':3, 'orange':12}
		warehouses  = [{'name': 'w1', 'inventory': { 'apple': 5, 'orange': 4 }}, { 'name': 'w2', 'inventory': { 'banana': 5, 'orange': 4 }},{ 'name': 'w3', 'inventory': { 'orange': 5 }} ]
		output = self.inventoryAllocator.allocate(order, warehouses)
		expected = [{'w1': {'apple': 3, 'orange': 4}}, {'w2': {'orange': 4}}, {'w3': {'orange': 4}}]
		self.assertEqual(output, expected)

	def test_case6(self):
		# Order can be shipped using multiple warehouses
		order = {'apple': 10}
		warehouses = [{'name': 'owd', 'inventory': { 'apple': 5 } }, { 'name': 'dm', 'inventory': { 'apple': 5 }}]
		output = self.inventoryAllocator.allocate(order, warehouses)
		expected = [{ 'owd': { 'apple': 5 }}, { 'dm': { 'apple': 5 } }]
		self.assertEqual(output, expected)

def main():
	# order = {'apple': 5, 'banana': 5, 'orange': 15}
	# warehouses  = [{'name': 'owd', 'inventory': { 'apple': 5, 'orange': 10 }}, { 'name': 'dm', 'inventory': { 'banana': 5, 'orange': 10 } } ]
	# inventoryAllocator = InventoryAllocator()
	# inventoryAllocator.allocate(order,warehouses)
	# t = TestInventoryAllocator()
	# t.setUp()
	# print(t.test_case1())
	unittest.main()


if __name__ == '__main__':
	main()