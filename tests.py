import unittest
import jack

# im really fed up with manually testing all the lines i write
# lets get to it

class JPrepareTests(unittest.TestCase):
	def test_prepare_results(self):
		result = jack.prepare("teacher")
		# test the result to see if its a generator
		pass

class JServeTests(unittest.TestCase):
	"""Tests for the serve() function."""
	
	def test_serve_result(self):
		"""Test that jack.serve() always returns a list."""
		result = jack.serve(["ate", "eat", "tea", "eta",])
		self.assertEqual(list, type(result))


unittest.main()