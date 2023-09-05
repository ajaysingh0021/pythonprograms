#
# Name: arr_multiply.py
# Purpose: 
# You have a input array on size n. 
# Replace each element position with multiplication of all other elements other than that at that position.
# Date: 5-Sep-23
#
# arr1 = [1,2,3,4]
arr1 = [1,-2,-3,4]
# out = [24,12,8,6]
out = []
product_all = 1
for i in arr1:
    product_all = product_all*i
# print(product_all)
for i in arr1:
    out.append(int(product_all/i))
print(out)

