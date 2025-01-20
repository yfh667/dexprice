list1 = [1,2,3,3,]
uni_list = list(set(list1))
print(uni_list)

list2 = [1,2,3,6,6]
uni_list2 = list(set(list2))


list3 = uni_list+uni_list2
print(list3)
uni_list3 = list(set(list3))
print(uni_list3)