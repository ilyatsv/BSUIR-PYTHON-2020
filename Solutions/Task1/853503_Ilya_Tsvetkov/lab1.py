import argparse
parser = argparse.ArgumentParser()
parser.add_argument ("task",type=int,help="choose your task",choices=[1,2,3,4,5])
parser.add_argument ('--adress',type=str,default = 'D:/1q.txt')
adress = parser.parse_args()
newword=""
dict = {}
final_dict={}
b=""
if adress.task==1:
 with open("{}".format(adress.adress)) as file_handler:
  word = file_handler.read()
 word+=" "
 word=word.replace('!','').replace('?','').replace('.','').replace(',','').replace(':','')
 listw=word.split()
 for element in listw:
    newword= element
    check = newword in dict
    if check==True:
        dict[newword]+=1
    else:
        dict[newword]=1
    newword=""
    continue
 print(dict)
if adress.task==2:
 with open("{}".format(adress.adress)) as file_handler:
  word = file_handler.read()
 word+=" "
#word=input()
 def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
 word=word.replace('!','').replace('?','').replace('.','').replace(',','').replace(':','')
 listw=word.split()
 for element in listw:
    newword= element
    check = newword in dict
    if check==True:
        dict[newword]+=1
    else:
        dict[newword]=1
    newword=""
    continue
 for v in range(10):
  if bool(dict)==True:
   max_value = max(dict.values())
   a=get_key(dict,max_value)
   b+=" "+a
   del dict[a]
  else:
   break
 print(b)
if adress.task==3:
 def partition(A, low, high) :
    pivot = A[high]
   
    i=low
    for j in range(low,high ):
     if A[j] <= pivot :
      k=A[j]
      A[j]=A[i]
      A[i]=k
      i += 1
    k=A[i]
    A[i]=A[high]
    A[high]=k
    return i
 def quicksort(A, low, high):
  if low < high :
   p = partition(A, low, high)
   quicksort(A, low, p - 1)
   quicksort(A, p + 1, high)
 MASS=[]
 with open("{}".format(adress.adress)) as file_handler:
    MASS2=(file_handler.read().split(" "))
 MASS = [int(item) for item in MASS2]   
 #MASS = [10,2,5,6,4,9,3,11,1,20,32,12,16,50]
 print(MASS)
 quicksort(MASS,0,len(MASS)-1)
 print(MASS)
if adress.task==4:
 def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i<len(lefthalf) and j<len(righthalf):
            if lefthalf[i]<righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i<len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j<len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
 with open("{}".format(adress.adress)) as file_handler:
  MASS2=(file_handler.read().split(" "))
 MASS = [int(item) for item in MASS2]   
#alist = [10,2,5,6,4,9,3,11,1,20,32,12,16,50]
 mergeSort(MASS)
 print(MASS)
def fibonacci(n):
        fib1, fib2 = 0, 1
        for i in range(n):
            fib1, fib2 = fib2, fib1 + fib2
            yield fib1
if adress.task==5:
  print(list(fibonacci(50)))
