from json import dumps, JSONEncoder, loads

def saveJson(fileName, obj):
	JSONEncoder().encode(obj)
	with open(fileName,"a") as file:
		file.write(dumps(obj, file, indent=4))

def readJson(fileName):
	with open(fileName, "r") as file:
		data = file.read()
		obj = loads(data)
	return obj
