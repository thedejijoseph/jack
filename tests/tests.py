import unittest
from .. import jack

# im really fed up with manually testing all the lines i write
# lets get to it

class JPrepareTests(unittest.TestCase):
	def test_prepare_results(self):
		result = jack.prepare("teacher")
		# test the result to see if its a generator
		pass

class JServeTests(unittest.TestCase):
	"""Tests for the serve() function."""
	
	def setUp(self):
		"""Set up a list of results for tests to work with."""
		
		self.test_order = ["ate", "eat", "tae", "tea", "eta"]
		self.result = ["ate", "eat", "eta", "tae", "tea"]
	
	def test_serve_result(self):
		"""Test that jack.serve() always returns a list."""
		
		result = jack.serve(self.test_order)
		self.assertEqual(type(self.result), type(result))
	
	def test_result_sort(self):
		"""Test that jack.serve() sorts its arguments."""
		
		result = jack.serve(self.test_order)
		self.assertEqual(self.result, result)


unittest.main()