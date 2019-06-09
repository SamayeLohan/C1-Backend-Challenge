#utility to add escape characters to given string input
inString = raw_input()

newString = ""

a = set(["\"", "/"])

for x in inString:
    cur = "\\"
    if x in a:
        cur = cur + x
    else:
        cur = x
    newString = newString + cur

print("\"" + newString + "\"")
