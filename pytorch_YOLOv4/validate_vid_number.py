"""
Given List: ["app","apple","appl","b","ball","ba","bal","cat","ca"]
Output List: ["apple","ball","cat"]
implement this in python
"""
def validate_vid_number(input_list):
    output_list = []

    if len(input_list) <= 0:
        return input_list

    list_len = len(input_list)
    x = input_list[0]
    for i in range(list_len):
        if x in input_list[i]:
            x = input_list[i]
        elif input_list[i] in x:
            continue
        else:
            output_list.append(x)
            x = input_list[i]
    output_list.append(x)

    return output_list


# input_list = ["app","apple","appl","b","ball","ba","bal","cat","ca"]
# print(validate_vid_number(input_list))