import math, operator

# alpha = 'abcdefghijklmnopqrstuvwxyz'
#
# values = {}
# i = 1
# for a in alpha:
#     values[a] = i
#     i += 1
#
# names = [1, 5, 'chakshu', 'pekka', 'punk', 'golem', 'tyagi']
# value_of_names = {}
# temp_val = 0
# for name in names:
#     if type(name) != int:
#         for char in name:
#             alpha_val = values[char]
#             temp_val += alpha_val
#
#         value_of_names[name] = temp_val
#         temp_val = 0


# def really_safe_normalise_in_place(d):
#     factor = 1.0 / math.fsum(d.t())
#     for k in d:
#         d[k] = d[k] * factor
#     key_for_max = max(d.iteritems(), key=operator.itemgetter(1))[0]
#     diff = 1.0 - math.fsum(d.itervalues())
#     # print "discrepancy = " + str(diff)
#     d[key_for_max] += diff
#     return d
#
#
# d = really_safe_normalise_in_place(value_of_names)
# print(d)

# temp = min(value_of_names.values())
# res = [key for key in value_of_names if value_of_names[key] == temp]
#
# print("Keys with minimum values are : " + str(res))

#


# try:
#     if '5' != 5:
#         raise "anError"
#     else:
#         print('an error has not occured')
# except Exception:
#     print('any error has occured')
