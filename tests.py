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
	def test_results(self):
		# results must always be a list
		result = jack.serve(["ate", "eat", "tea", "eta",])
		self.assertEqual(list, type(result))


unittest.main()