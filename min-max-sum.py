# Mini-Max Sum
# Given five positive integers, find the minimum and maximum values that can be calculated by summing exactly four of the five integers. 
# Then print the respective minimum and maximum values as a single line of two space-separated long integers.
#

arr = [9,3,5,7,1]
arr.sort()
# print(arr)
# print(arr[1:])
# print(arr[:-1])
print(sum(arr[:-1]), sum(arr[1:]))