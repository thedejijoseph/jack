# for a before and after test of applying multithreading

import requests
import threading

# long running orders
orders = ["cholesterol", "ambiguously", "bonaventura", "dyslexia", "empathetically", "fundamental"]

def shoot(order):
	r = requests.get(f"http://localhost:3303/serve?order={order}")

for order in orders:
	threading.Thread(target=shoot, args=[order]).start()
