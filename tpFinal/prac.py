def nthNearestPalinDrome(n,start):
    found = 0
    guess = start
    lo = start
    hi = start
    lst  = []
    if n == 0:
        return start

    while found < n:

        lo -= 1
        hi += 1
        if isPalin(lo) and isPalin(hi):
            found += 1
            lst.append(max(lo,hi))

        elif isPalin(lo):
            found += 1
            lst.append(lo)
        elif isPalin(hi):

            found += 1
            lst.append(hi)
        

    return lst[-1]

def isPalin(num):

    s = str(num)
    if s[0] == s[2]:
        return True

    return False

print(nthNearestPalinDrome(1,126))