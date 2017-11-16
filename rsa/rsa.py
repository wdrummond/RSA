import random
import math
import monte


def ToBase10(string, alphabet, base):
	# # returns the base 10 equivalent
	# for k, v in enumerate(alphabet):
	# 	print(k, v)
	return sum(alphabet.index(x)*(base**i) for i, x in enumerate(string[::-1]))
			

def FromBase10(integer, alphabet):
	# return a string in the given alphabet
	alphadict = {}
	for k, v in enumerate(alphabet):
		alphadict[k] = v
	#betadict = dict(map(reversed, alphadict.items()))

	array = []
	while integer:
		integer, value = divmod(integer, len(alphabet))
		array.append(alphadict[value])
	return ''.join(reversed(array))


def egcd(a, b):
	x,y, u,v = 0,1, 1,0
	while a != 0:
		q, r = b//a, b%a
		m, n = x-u*q, y-v*q
		b,a, x,y, u,v = a,r, u,v, m,n
	gcd = b
	if y<0:
		y += a
	return y
	#return gcd, x, y

class RSA:

	def __init__(self):
		return

	def GenerateKeys(self, p_string, q_string):
		#Treat the text strings as base 26 numbers, 
		#and convert them to base 10 numbers.
		alphabet1="abcdefghijklmnopqrstuvwxyz"
		p = ToBase10(p_string, alphabet1, 26)
		q = ToBase10(q_string, alphabet1, 26)
		#p = int(p, 10)
		#q = int(q, 10)

		#mod by 10^200 to make them the right size.
		p %= 10**200
		q %= 10**200

		#Make them odd.
		if p%2==0:
			p += 1
		if q%2==0:
			q += 1

		#Then start adding 2 until they are prime.
		while not monte.IsPrimeMonteCarlo(p):
			p += 2
		while not monte.IsPrimeMonteCarlo(q):
			q += 2

		#Calculate n = p*q
		#Calculate r = (p-1)*(q-1)
		n = p * q
		r = (p-1) * (q-1)

		#Find e – a 100 digit prime number that does not evenly divide into r.
		#Find d – the inverse of e mod r.
		e = random.randrange(1, r)

		#while not isPrimeMonte(e) or e % r = 0
		while not monte.IsPrimeMonteCarlo(e) or e % r == 0:
			e = random.randrange(1, r)
		d = egcd(r, e)
		print("Checking d:",e*d%r)

		#Save n and e to a file called public.txt (write them as text, with 1 return after each number)
		f = open('public.txt', 'w')
		f.write(str(n))
		f.write('\n')
		f.write(str(e))
		f.write('\n')
		f.close()

		#Save n and d to a file called private.txt
		f = open('private.txt', 'w')
		f.write(str(n))
		f.write('\n')
		f.write(str(d))
		f.write('\n')
		f.close()

		return

		#return ((n, e), (n, d))



	def Encrypt(self, infile, outfile, publickeyfile):
		#get public keys
		f = open(publickeyfile, 'r')
		n = int(f.readline())
		e = int(f.readline())
		f.close()

		#Use this alphabet: alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.?! \t\n\r"
		alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.?! \t\n\r"

		#Open the input file (which should already exist in the current directory and be full of plain text).
		inf = open(infile, 'rb')
		outf = open(outfile, 'wb')

		#Treat the input file text as a base 70 integer, and convert it to base 10, using block sizes so as to not exceed integer n.
		pltext = inf.read()		
		inf.close()
		pltext = pltext.decode("utf-8")

		#Encode each block using the rules of RSA.  (Read n and e from public.txt)
		#calculate block size
		max_block_size = math.floor(math.log(n) / math.log(len(alphabet)))
		print("max_block_size is",max_block_size)
		num_blocks = (len(pltext) - 1) // max_block_size + 1

		for b in range(num_blocks):
			current_block = pltext[b*max_block_size:(b+1)*max_block_size]
			x = ToBase10(current_block, alphabet, len(alphabet))

			# Let x be a block of the plaintext file, converted to an integer
			C = pow(x,e,n) # This encrypts x to C. This does (x**e)%n

			encryptedmessage = FromBase10(C, alphabet)
			outf.write((encryptedmessage +"$").encode("utf-8"))

		outf.close()

	def Decrypt(self, infile, outfile, privatekeyfile):
		#get private keys
		f = open(privatekeyfile, 'r')
		n = int(f.readline())
		d = int(f.readline())
		f.close()

		#get alphabet
		alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.?! \t\n\r"

		fin = open(infile, 'rb')
		fout = open(outfile, 'wb')

		enctext = fin.read()
		fin.close()
		enctext = enctext.decode("utf-8")
		x = ''

		for i in range(len(enctext)):
			if enctext[i] == '$':
				x = ToBase10(x, alphabet, len(alphabet))
				C = pow(x,d,n) # This decrypts x to C. This does (x**d)%n
				decryptedmessage = FromBase10(C, alphabet)
				fout.write((decryptedmessage).encode("utf-8"))
				x = ''

			else: # if enctext[i] != '$':
				x += enctext[i]

		fout.close()

def main():
	# p = ToBase10("stop", "abcdefghijklmnopqrstuvwxyz", 26)
	# print("p in base 10 is: ", p)
	# s = FromBase10(p, "abcdefghijklmnopqrstuvwxyz")
	# print("converted back from base 10 is: ", s)

	# p = ToBase10("Hey does this work for real?!", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.?! \t\n\r", 70)
	# print("p in base 10 is: ", p)
	# s = FromBase10(p, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.?! \t\n\r")
	# print("converted back from base 10 is: ", s)

	rsa = RSA()
	#p = input("Enter your first string: ")
	#q = input("Enter another string: ")
	#print("Generating your public/private keys now . . .")
	#rsa.GenerateKeys(p, q)
	#rsa.Encrypt('WyattEncrypted.txt','encrypted.txt', 'public.txt')
	rsa.Decrypt('wencrypted.txt', 'BartDecrypted.txt', 'private.txt')

main()

####text keys####
#   hejihmlfohkizpquvzhsvvbwwgpyfzqunuqclckyrkpufvmfszgklccguupheeohckotlqqeqleomcjbpzisugwxebawtqhcrrqk

#   rccsjgochlozcykjpwvccoizmuukoyqmpsaotvjybokshfsekqsbairoftewlzymucyuxwianstmepczgnfmplzpbhfjgixavlku

#finding blocks sizes
#b = math.ceil(float(x)/y +1)
