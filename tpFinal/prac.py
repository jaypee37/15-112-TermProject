def mostFrequentLetters(s):
	s = s.lower()
	s = s.replace(" ","")
	r = ""
	for i in s:
		if not i.isalpha():
			continue
		else:
			r+= i
	
	s = r
	
	s = sorted(s)
	print(s)

	result = "" + s[0]
	#teanioscdhpruglw

	for i in range(1,len(s)):
		cur = s.count(s[i])

		if s[i] not in result:
			for j in range(len(result)):
				if j == len(result) -1:
					result += s[i]
					continue
				if cur <= s.count(result[j]) and cur > s.count(result[j+1]):
					
					result = result[:j] + s[i] + result[j:]
					break
				print(result)
	print(result)
	return result
def testMostFrequentLetters():
    print("Testing mostFrequentLetters()...", end="")
    assert(mostFrequentLetters("We attack at Dawn") == "atwcdekn")
    s = "Note that digits, punctuation, and whitespace are not letters!"
    assert(mostFrequentLetters(s) == "teanioscdhpruglw")
    assert(mostFrequentLetters("") == "")
    print("Passed.")

#print(mostFrequentLetters("We Attack at Dawn"))
#atwcdekn
#w
testMostFrequentLetters()
