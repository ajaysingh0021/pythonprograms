#
# Name: lonely_integer.py
#
# Given an array of integers, where all elements but one occur twice, find the unique element.
#

def lonelyinteger(a):
    # Write your code here
    test_dict = {}
    for num in a:
        test_dict[num] = test_dict.get(num, 0) + 1
    for k,v in test_dict.items():
        if v == 1:
            return k
        

if __name__ == '__main__':
    arr = [1,1,2]
    arr = [0,0,2,5,2,3,3]

    result = lonelyinteger(arr)

    print(str(result) + '\n')

