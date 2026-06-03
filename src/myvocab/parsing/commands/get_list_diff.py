def get_list_diff(list1: list, list2: list) -> list:
    """ Get the difference between list1 and list2. """

    list_return = list()
    if list1 and not list2:
        return list(list1)
    elif list1 and list2:
        for item1 in list1:
            if item1 not in list2:
                # If the item1 is in list1 but not in list2
                list_return.append(item1)

    return list_return