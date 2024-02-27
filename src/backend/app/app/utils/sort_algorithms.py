def quickSort(array):
    if len(array) > 1:
        pivot = array.pop()
        grtr_lst, equal_lst, smlr_lst = [], [pivot], []
        for item in array:
            if item == pivot:
                equal_lst.append(item)
            elif item > pivot:
                grtr_lst.append(item)
            else:
                smlr_lst.append(item)
        return quickSort(smlr_lst) + equal_lst + quickSort(grtr_lst)
    else:
        return array


def sort_with_refrence(items, refrence, presorted: bool = False):
    if not presorted:
        sorted_refrence = quickSort(refrence.copy())
    else:
        sorted_refrence = refrence

    sorted_items = ["filler"] * len(items)
    for obj, column_value in zip(items, refrence):
        ind = sorted_refrence.index(column_value)
        sorted_items[ind] = obj

    return sorted_items
