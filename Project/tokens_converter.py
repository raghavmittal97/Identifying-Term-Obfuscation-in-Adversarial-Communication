
def string_to_token(string):
	tokens = string.split(" ")
	tokens = [token.replace(',','').replace('.','') for token in tokens] #removing fullstops, commas
	return tokens
	
print(string_to_token("hello,."))