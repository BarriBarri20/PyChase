test_dict = {2:[4,5,6, 0, 2, 0, 34, 32]}

test_dict[2].sort()
test_dict[2].sort(key= lambda x: x==0)

print(test_dict[2])