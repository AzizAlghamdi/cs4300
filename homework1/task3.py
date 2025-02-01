def check_number(num):
	if num > 0:
		return "Postive"
	elif num < 0:
		return "Negative"
	else:
		return "Zero"
def first_10_primes():
	primes = []
	num = 2
	while len(primes) < 10:
		if all(num % p !=0 for p in primes):
			primes.append(num)
		num += 1
	return primes

def sum_1_to_100():
	return sum(range(1, 101))

