# for a before and after test of applying multithreading

import requests
import json
import threading

# long running orders
orders = ["choker", "ambient", "bonafide", "dyslexia", "empathy", "funday"]

def shoot(order):
	# now to check received responses for correlation
	print(f"firing {order}")
	r = json.loads(requests.get(f"http://localhost:3303/serve?order={order}").text)
	i = True if order in set(r['serving']) else False
	print(f"acquired {order}: {r['time_taken']}; {r['serving'][-6:]}")
	

for order in orders:
	threading.Thread(target=shoot, args=[order]).start()
