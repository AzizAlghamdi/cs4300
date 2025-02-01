import task2

def test_data_types():
	data = task2.get_data_types()
	assert isinstance(data["integer"], int)
	assert isinstance(data["float"], float)
	assert isinstance(data["string"], str)
	assert isinstance(data["boolean"], bool)
