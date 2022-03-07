"""
To sort this type of list 
[(377, 292, 412, 344), (413, 292, 448, 343), (153, 286, 204, 338), (340, 
294, 377, 343), (216, 288, 252, 339), (449, 290, 488, 348), (252, 287, 288, 341), (293, 291, 330, 342)]

(x1,y1,x2,y2)
"""

def sort_x(input_list):
    len_of_list = len(input_list)
    for i in range(0,len_of_list):
        for j in range(0, len_of_list-i-1):
            # check for single row
            if(input_list[j][0] > input_list[j+1][0]):
                temp = input_list[j]
                input_list[j] = input_list[j+1]
                input_list[j+1] = temp
    return input_list


def sort_tuple_in_list(input_list):
    check_2_row = False
    len_of_list = len(input_list)
    for i in range(0,len_of_list):
        for j in range(0, len_of_list-i-1):
            # check for single row
            if(input_list[j][1] - input_list[j+1][1] > 10):
                check_2_row = True
                temp = input_list[j]
                input_list[j] = input_list[j+1]
                input_list[j+1] = temp 
    lower_len = len_of_list-4
    lower_list = input_list[lower_len:len_of_list]
    lower_list_sorted = sort_x(lower_list)
    # print(lower_list)
    # print(lower_list_sorted)
    upper_list = input_list[0:lower_len]
    upper_list_sorted = sort_x(upper_list)
    # print(lower_list)
    # print(lower_list_sorted)
    
    if check_2_row == True:
        output_list = upper_list_sorted + lower_list_sorted
    else:
        output_list = sort_x(input_list)

    return (output_list,(upper_list_sorted,lower_list_sorted,check_2_row))

# list = [(377, 292, 412, 344), (413, 292, 448, 343), (153, 286, 204, 338), (340,294, 377, 343), (216, 288, 252, 339), (449, 290, 488, 348), (252, 287, 288, 341), (293, 291, 330, 342)]

list = [(1875, 1763, 1952, 1909), (1803, 1765, 1877, 1914), (1703, 1936, 1867, 2129), (1896, 1920, 2041, 2121), (1623, 1770, 1756, 1926), (1519, 1945, 1687, 2149), (1976, 1745, 2078, 1900), (2055, 1918, 2216, 2096)]


# print(sort_tuple_in_list(list))