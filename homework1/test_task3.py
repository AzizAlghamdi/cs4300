import task3

def test_check_number():
	assert task3.check_number(10) == "Postive"
	assert task3.check_number(-5) == "Negative"
	assert task3.check_number(0) == "Zero"

def test_first_10_primes():
	assert task3.first_10_primes() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_sum_1_to_100():

	assert task3.sum_1_to_100() == 5050
