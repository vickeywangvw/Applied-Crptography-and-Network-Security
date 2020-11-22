import math
import random
import re  
import os
def write_random(file):
    os.remove(file)
    f = open(file, 'wt' ,encoding="utf-8")
    f.write('Line:133'+'\n')
    b=[]
    for i in range(31,-1,-1):
        if(i>6):
            b.append(0)
        elif(i==6 or i==0):
            #bit no.0 and bit no.6
            b.append(1)
        else:
            a=random.randint(561,999)
            #randomly generate integers from 561 to 999
            if(a%2):
                b.append(1)
                f.write('b_'+str(i)+'|'+str(bin(a)[2:])+'|1'+'\n')
                #if the integer is odd, the least significant bit will be 1
            else:
                b.append(0)
                f.write('b_'+str(i)+'|'+str(bin(a)[2:])+'|0'+'\n')
                #if the integer is even, the least significant bit will be 0
    s="".join('%s' %id for id in b)
    f.write('Number|'+str(int(s,2))+'|'+s+'\n')
    f.close()
    return(int(s,2))

def generate_random_num():
    #generate 7-bit random number and sotre it as a 32 bits integer with leading 0s
    #bit no.0 and no.6 should be 1, 0 will fill from bit no.7 to bit no.31
    #value of other bits will be generated randomly
    b=[]
    for i in range(31,-1,-1):
        if(i>6):
            b.append(0)
        elif(i==6 or i==0):
            #bit no.0 and bit no.6
            b.append(1)
        else:
            a=random.randint(561,999)
            #randomly generate integers from 561 to 999
            if(a%2):
                b.append(1)
                #print('b_'+str(i)+'|'+str(bin(a)[2:])+'|1')
                #if the integer is odd, the least significant bit will be 1
            else:
                b.append(0)
                #print('b_'+str(i)+'|'+str(bin(a)[2:])+'|0')
                #if the integer is even, the least significant bit will be 0
    s="".join('%s' %id for id in b)
    #print('Number|'+str(int(s,2))+'|'+s)
    return(int(s,2))

        
##Miller-Rabin Algorithm
def quickMult(a, b, c):
    #Binary Exponentiation calculates (a*b)%c
    result = 0
    while b > 0:
        if b & 1:
            result = (result + a) % c
        a = (a + a) % c
        b >>= 1
    return result

def quickPower(a, b, c):
    result = 1
    while b > 0:
        if (b & 1):
            result = quickMult(result, a, c)
        a = quickMult(a, a, c)
        b >>= 1
    return result
 
def MillerRabinPrimeTest(n):
    #test whether the 7-bit random number is a prime
    a = random.randint(1,n-1) 
    #randomly select a integer a,such that 0<a<n
    s = 0 
    #s is the number of factor 2
    d = n - 1
    while (d & 1) == 0: 
        #extract all factor 2 in d
        s += 1
        d >>= 1
 
    x = quickPower(a, d, n)
    for i in range(s): 
        #secondary prime detection
        newX = quickPower(x, 2, n)
        if newX == 1 and x != 1 and x != n - 1:
            return False 
            # n is not a prime
        x = newX
 
    if x != 1:
        #x=a^(n-1) (mod n),n is not a prime
        return False
 
    return True  

def isPrintPrimeByMR(path,n):
    f = open(path, 'a+' ,encoding="utf-8")
    if ((n & 1) == 0 or n % 5 == 0):
        f.write(str(n)+'is not a prime'+'\n')
        return False
    for i in range(20):
        #take Miller-Rabin test for 20 times
        if MillerRabinPrimeTest(n) == False:
            f.write(str(n)+' is not a prime'+'\n')
            return False
    f.write(str(n)+' is perhaps a prime'+'\n')
    f.write('\n')
    f.close()
    return True
def isPrimeByMR(n):
    if ((n & 1) == 0 or n % 5 == 0):
        return False
    for i in range(20):
        #take Miller-Rabin test for 20 times
        if MillerRabinPrimeTest(n) == False:
            return False
    return True
def find_prime():
    #check wheher the 7-bit random number is a prime or not
    rand_num=generate_random_num()
    if(isPrimeByMR(rand_num)):
        return(rand_num) 
def find_print_prime(file):
    #check wheher the 7-bit random number is a prime or not
    rand_num=write_random(file)
    if(isPrimeByMR(rand_num)):
        return(rand_num) 
def get_prime():
    p=find_prime()
    while(p is None):
        p=find_prime()
        #if the selected random number is not a prime, then select another one and check again
    return p
def get_print_prime(file):
    p=find_print_prime(file)
    while(p is None):
        p=find_print_prime(file)
        #if the selected random number is not a prime, then select another one and check again
    return p
#extended encludean algorithm
def gcd(a,b):
    if(a<b):
        temp=a
        a=b
        b=temp
    if (a%b)==0:
        return b
    else:
        return gcd(b,a%b)
def EX_GCD(a,b,arr):
    if b == 0:
        arr[0] = 1
        arr[1] = 0
        return a
    g = EX_GCD(b, a % b, arr)
    t = arr[0]
    arr[0] = arr[1]
    arr[1] = t - int(a / b) * arr[1]
    return g
def ModReverse(a,n):
    #find the multiplicative inverse
    arr = [0,1,]
    gcd = EX_GCD(a,n,arr)
    if gcd == 1:
        return (arr[0] % n + n) % n
    else:
        return -1
def get_public_key(n):
    e=3
    #print('e ='+str(e))
    while(gcd(e,n)!=1):
        #if e is not relatively prime with fai(n), choose another e by add 1 to the original e
        e+=1
    return e
def get_private_key(e,n):
    return ModReverse(e,n)
def XOR_BinString(s):
    h=re.findall(r'.{8}',s)
    #partition s into bytes 
    num=len(s)//8
    for i in range(0,num-1):
        b=''
        for j in range(0,8):
            #compute their XOR by bit
            temp=str(int(h[i][j])^int(h[i+1][j]))
            #the first byte XOR with the second one, use the result to do XOR with the third one
            #until finishing computing all bytes, then the last byte will be our XOR¡¡result
            b+=temp
        h[i+1]=b
    return b
def modExp(a,exp,mod):
    fx=1
    while exp>0:
        if(exp&1)==1:
            fx=fx*a%mod
        a=(a*a)%mod
        exp=exp>>1
    return fx
def print_modExp(path,a, exp, mod): 
    #fast exponentiation
    f = open(path, 'a+' ,encoding="utf-8")
    exp11=bin(exp)
    k=len(exp11)
    y = 1
    f.write('i|xi|y|y'+'\n')
    for i in range(2,k):
        y = y * y % mod
        temp=y
        if (int(exp11[i]) == 1):
            y = a * y % mod
            temp2=y
            f.write(str(k-1-i)+' |'+str(exp11[i])+' |'+str(temp)+' |'+str(temp2)+' |'+'\n')
        else:
            f.write(str(k-1-i)+' |'+str(exp11[i])+' |'+str(temp)+' |'+str(y)+' |'+'\n')
    f.close()
    return y
def main():
    for i in range(0,20):
        path='g:/output'+str(i+1)+'.txt'
        #one of the prime numbers 
        get_print_prime(path)
        file = open(path, 'a+' ,encoding="utf-8")
        file.write('\n')
        file.write('Line:149'+'\n')
        file.close()
        isPrintPrimeByMR(path,generate_random_num())
        file = open(path, 'a+' ,encoding="utf-8")
        file.write('Line:155'+'\n')
        file.close()
        isPrintPrimeByMR(path,generate_random_num())  
        file = open(path, 'a+' ,encoding="utf-8")
        file.write('Line:174'+'\n')
        file.write('Line:186'+'\n')
        #For Alice,show p,q,n,e,d
        p=get_prime()
        q=get_prime()
        while(p==q):
            p=get_prime()
            q=get_prime()
        if(p!=q):
            fai=(p-1)*(q-1)
            n=p*q
            e=get_public_key(n)
            d=get_private_key(e,n)
        file.write('Line:190'+'\n')
        file.write('p = '+str(p)+','+'q = '+str(q)+','+'n = '+str(n)+','+'e ='+str(e)+','+'d = '+str(d)+'\n')
        file.write('p = '+("{:#032b}".format(p)).replace('b','0')+'\n')
        file.write('q = '+("{:#032b}".format(q)).replace('b','0')+'\n')
        file.write('n = '+("{:#032b}".format(n)).replace('b','0')+'\n')
        file.write('e = '+("{:#032b}".format(e)).replace('b','0')+'\n')
        file.write('d = '+("{:#032b}".format(d)).replace('b','0')+'\n')
        file.write('\n')       
        #For Trent,show p,q,n,e,d
        p_T=get_prime()
        q_T=get_prime()
        while(p_T==q_T):
            p_T=get_prime()
            q_T=get_prime()
        if(p_T!=q_T):
            fai_T=(p_T-1)*(q_T-1)
            n_T=p_T*q_T
            e_T=get_public_key(n)
            d_T=get_private_key(e,n)
        else:
            q_T=get_prime() 
            fai_T=(p_T-1)*(q_T-1)
            n_T=p_T*q_T
            e_T=get_public_key(n)
            d_T=get_private_key(e,n)
        file.write('Line:198'+'\n')
        file.write('p = '+str(p_T)+','+'q = '+str(q_T)+','+'n = '+str(n_T)+','+'e ='+str(e_T)+','+'d = '+str(d_T))
        file.write('p = '+("{:#032b}".format(p_T)).replace('b','0')+'\n')
        file.write('q = '+("{:#032b}".format(q_T)).replace('b','0')+'\n')
        file.write('n = '+("{:#032b}".format(n_T)).replace('b','0')+'\n')
        file.write('e = '+("{:#032b}".format(e_T)).replace('b','0')+'\n')
        file.write('d = '+("{:#032b}".format(d_T)).replace('b','0')+'\n')
        file.write('\n')   
        #computing r,h(r),s
        file.write('Line:222'+'\n')
        s1=''.join([bin(ord(c)).replace('0b', '0') for c in ' Alice'])
        #1-6 bytes: Alice padded with space 
        s2=("{:#032b}".format(8611)).replace('b','0')
        #7-10 bytes: n 32 bits
        s3=("{:#032b}".format(5)).replace('b','0')
        #11-14 bytes: e 32 bits
        r='0'+s1+s2+s3
        file.write('r = '+r+'\n')
        s4=("{:#032b}".format(int(XOR_BinString(r),2))).replace('b','0')
        #h(r) 32 bits
        file.write('h(r) = '+s4+'\n')
        file.write('\n')
        file.write('Line:224'+'\n')
        h_int=int(XOR_BinString(r),2)
        file.write('h(r) = '+str(h_int)+','+'s = '+'\n')
        file.write('\n')
        #computing k and u
        file.write('Line:246'+'\n')
        s5=("{:#032b}".format(n)).replace('b','0')
        for i in range(0,32):
            if int(s5[i])==1:
                #get the position(which is k) of the first 1
                k=31-i
                break
        left=2**(k-1)+2**0
        #leading 0s & 1111111
        right=2**(k)-2**0
        #leading 0s & 1000001
        #u is in range(left,right)
        u=random.randint(left,right)
        file.write('k = '+str(k)+','+'u ='+str(u)+'\n')
        file.write('\n')
        file.write('Line:246'+'\n')
        s6=("{:#032b}".format(u)).replace('b','0')
        file.write('u = '+s6+'\n')
        file.write('\n')
        file.write('Line:254'+'\n')
        s7=("{:#032b}".format(int(XOR_BinString(s6),2))).replace('b','0')
        v=modExp(int(XOR_BinString(s6),2),p,n)
        Ev=modExp(v,e,n)
        file.write('u = '+str(u)+','+'h(u) = '+str(int(XOR_BinString(s6),2))+','+'v = '+str(v)+','+'Ev = '+str(Ev)+'\n')
        file.write('\n')
        file.write('Line:257'+'\n')
        file.close()
        print_modExp(path,v,e,n)
main()