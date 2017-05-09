from json import dumps, JSONEncoder

def saveJson(fileName, object):
	JSONEncoder().encode(object)
	with open(fileName,"a") as file:
		file.write(dumps(object, file, indent=4))