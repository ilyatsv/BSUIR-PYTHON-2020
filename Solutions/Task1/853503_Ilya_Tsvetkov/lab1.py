import argparse
parser = argparse.ArgumentParser()
parser.add_argument ("task",type=int,help="choose your task",choices=[1,2,3,4,5])
parser.add_argument ("--number",type=int,help="choose fibonacci's number",default=50)
parser.add_argument ('--adress',type=str,default = 'D:/1q.txt')
adress = parser.parse_args()
def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
def partition(A, low, high):
    pivot = A[high]
    i = low
    for j in range(low,high ):
        if A[j] <= pivot:
            k = A[j]
            A[j] = A[i]
            A[i] = k
            i += 1
    k = A[i]
    A[i] = A[high]
    A[high] = k
    return i
def quick_sort(A, low, high):
    if low < high :
        p = partition(A, low, high)
        quick_sort(A, low, p - 1)
        quick_sort(A, p + 1, high)
def merge_sort(alist):
    if len(alist) > 1:
        mid = len(alist)//2
        left_half = alist[:mid]
        right_half = alist[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = 0
        j = 0
        k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                alist[k] = left_half[i]
                i = i + 1
            else:
                alist[k] = right_half[j]
                j = j + 1
            k = k+1

        while i < len(left_half):
            alist[k] = left_half[i]
            i = i + 1
            k = k + 1

        while j < len(right_half):
            alist[k] = right_half[j]
            j = j + 1
            k = k + 1
def fibonacci(n):
        fib_1, fib_2 = 0, 1
        for i in range(n):
            fib_1, fib_2 = fib_2, fib_1 + fib_2
            yield fib_1
new_word = ""
dict = {}
final_dict = {}
b =""
if adress.task == 1:
    with open("{}".format(adress.adress)) as file_handler:
        word = file_handler.read()
    word += " "
    word = word.replace('!','').replace('?','').replace('.','').replace(',','').replace(':','')
    listw = word.split()
    for element in listw:
        new_word = element
        check = new_word in dict
        if check == True:
            dict[new_word] += 1
        else:
            dict[new_word] = 1
        new_word = ""
        continue
    print(dict)
if adress.task == 2:
    with open("{}".format(adress.adress)) as file_handler:
        word = file_handler.read()
    word += " "
    word = word.replace('!','').replace('?','').replace('.','').replace(',','').replace(':','')
    listw = word.split()
    for element in listw:
        new_word = element
        check = new_word in dict
        if check == True:
            dict[new_word] += 1
        else:
            dict[new_word] = 1
        new_word = ""
        continue
    for v in range(10):
        if bool(dict) == True:
            max_value = max(dict.values())
            a = get_key(dict,max_value)
            b += " " + a
            del dict[a]
        else:
            break
    print(b)
if adress.task == 3:
    Mass = []
    with open("{}".format(adress.adress)) as file_handler:
        Mass_2 = (file_handler.read().split(" "))
    Mass = [int(item) for item in Mass_2]   
    #MASS = [10,2,5,6,4,9,3,11,1,20,32,12,16,50]
    print(Mass)
    quick_sort(Mass,0,len(Mass)-1)
    print(Mass)
if adress.task == 4:
    with open("{}".format(adress.adress)) as file_handler:
        Mass_2=(file_handler.read().split(" "))
    Mass = [int(item) for item in Mass_2]   
    #alist = [10,2,5,6,4,9,3,11,1,20,32,12,16,50]
    merge_sort(Mass)
    print(Mass)

if adress.task == 5:
  print(list(fibonacci(adress.number)))
