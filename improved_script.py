#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#1 Write a Python program to get the Python version you are using and print it out
import sys
print("Python version:")
print (sys.version)
print (sys.platform)


# In[ ]:


print("Python version:", end=" ")
print (sys.version)


# In[ ]:


print("Python version: " + sys.version)
print("Python version: ", sys.version, sep="")
print("Python version: %s" %sys.version)
print("Python version: {0}".format(sys.version))


# In[ ]:


#2 Write a Python program to print the following as shown
print("Baa, baa, black sheep \n\t\t Have you any wool? \n\t Yes sir, yes sir \n\t\t\t Three bags full. \n One for my master \n\t And one for the dame \n One for the little boy \n Who lives down the lane.")


# In[ ]:


print("Baa, baa, black sheep", end="\n")
print("\t\t Have you any wool?")
print("\t Yes sir, yes sir ")
print("\t\t\t Three bags full. ")
print("One for my master ")
print("\t And one for the dame")
print("One for the little boy ")
print(" Who lives down the lane.")


# In[ ]:


message = "Baa, baa, black sheep \n\t\t Have you any wool? \n\t Yes sir, yes sir \n\t\t\t Three bags full. \n One for my master \n\t And one for the dame \n One for the little boy \n Who lives down the lane."
print (message)


# In[ ]:


#3 Write a Python program to count the number of even and odd numbers from a series of numbers
numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15) # Declaring the tuple
even = len(numbers)//2
odd = len(numbers) - even

print("Number of even numbers is", even)
print("Number of odd numbers is", odd)


# In[ ]:


import random as rnd
numbers =[int(rnd.random()*100) for i in range(15)] # Declaring the tuple
print(numbers)
odd = 0
even = 0
for num in numbers:
  if not num % 2: #if num % 2 ==0: #0 is False / Even, 1 is True / Odd
    even+=1
  else:
    odd+=1
print("Number of even numbers is", even)
print("Number of odd numbers is", odd)


# In[ ]:


#4 Write a Python program that prints all the numbers from 0 to 50 except 37 and 16
numbers=list(range(51))
print (numbers)
numbers.remove(16)
numbers.remove(37)
print(numbers)


# In[ ]:


for x in range(51):
  if (x == 37 or x==16):
    continue
  #print(x)
  print(x,end=" ")


# In[ ]:


#5 Write a Python program to get the Fibonacci series between 0 and 100. 
#The Fibonacci Sequence is the series of numbers: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
# 0, 1, 1 (1+0), 2(1+1), 3(2+1), 5(3+2), 8(5+3), 13(8+5), 21(13+8), 34(21+13), ... y = y + old
#The next number is found by adding up the two numbers before it.
old = 0
y = 1
while(y<100):
  print(y, end=" ")
  t = old
  old = y
  y = y + t


# In[ ]:


x,y=0,1
while y<100:
  print(y, end=" ")
  x,y = y,x+y


# In[ ]:


x = 0
y = 1
print (x, y)
x,y = y,x
print (x, y)
x = y
y = x
print (x,y)


# In[ ]:




