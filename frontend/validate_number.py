my_char = 'ba25pa12345'
pos_ba = my_char.find('ba')
pos_pa = my_char.find('pa')
# print(len(my_char[pos_ba+2:pos_pa]))
# print(int(my_char[pos_ba+2:pos_pa]))
# print(len(my_char[pos_pa+2:]))
if(len(my_char[pos_pa+2:])<=4):
    try: 
        print(int(my_char[pos_pa+2:]))
    except:
        print("Not a number")
else:
    print("more than 4 chars detected")