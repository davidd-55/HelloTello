import os

def cascade_finder():

    cascade_list = []
    num = 0
    dir_path = os.path.dirname(os.path.realpath(__file__))
    directory = dir_path + "/cascades"

    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            num += 1
            modified_name = str(num) + ". " + filename[12:-4]
            cascade_list.append(modified_name)

    return cascade_list

def usr_choice(lst):
    lst_size = len(lst)

    try:
        usr_selec = input("Type the number for your selection:\n\t")
        while not int(usr_selec) > 0 or not int(usr_selec) < (lst_size + 1):
            usr_selec = input("Invalid or out-of-range choice. Try again:\n\t")

    except ValueError:
        return usr_choice(lst)

    user_filename = lst[(int(usr_selec) - 1)]
    
    if int(usr_selec) > 9:
        user_filename_modified = "haarcascade_" + user_filename[4:] + ".xml"
    else:
        user_filename_modified = "haarcascade_" + user_filename[3:] + ".xml"
    
    return user_filename_modified

cas_lst = cascade_finder()
print("Available objects for tracking:")
for name in cas_lst:
    print(name)
print(usr_choice(cas_lst))
            