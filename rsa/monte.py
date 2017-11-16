import math
import random

def IsPrimeMonteCarlo(n):
	for i in range(10):
		b = random.randrange(2, n)
		ok = millersTest(n, b)
		if not ok:
			return False
	return True

def millersTest(n, b):
	s = 0
	t = n - 1
	while t % 2 == 0:
		t = t // 2
		s += 1
	if pow(b, t, n) == 1:
		return True
	for j in range(s):
		if pow(b, t, n) == n - 1:
			return True
		t *= 2
	return False

def IsPrime(x):
	if x >= 2:
		for y in range(2,int(math.sqrt(x)+1)):
			if not ( x % y ):
				return False
	else:
		return False
	return True


if __name__ == "__main__":
	#ins = int(input("Input your number: "))
	#print(IsPrimeMonteCarlo(ins))
		for i in range(3, 1000001):
				p1 = IsPrimeMonteCarlo(i)
				p2 = IsPrime(i)
				if p1 != p2:
						print("Error on integer " + str(i))

		print("Done")
                
#main()


## 200 digit prime numbers:
## 74478580750838202831824053069974345053332119076247119928686899724159033682278623912236628767219870499181401157263469983181319722599485472309515237651592891231333888800351664791513651463122923408151087
## 41878087056733099756382881656795724370735116244908662151856774333009153897791573627099704389697245213731425734276664250226562926645404728649959013809715926709940411123134625310761352302877087575114519
