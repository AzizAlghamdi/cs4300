def count_words(filename):
	with open(filename, "r") as file:
		return len(file.read().split())

