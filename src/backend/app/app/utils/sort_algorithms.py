from typing import Any, List


def quickSort(array: List[Any]) -> List[Any]:
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


def sort_with_refrence(
    items: List[Any], reference: List[Any], presorted: bool = False
) -> List[Any]:
    if not presorted:
        sorted_refrence = quickSort(reference.copy())
    else:
        sorted_refrence = reference

    sorted_items = ["filler"] * len(items)
    for obj, column_value in zip(items, reference):
        ind = sorted_refrence.index(column_value)
        sorted_items[ind] = obj

    return sorted_items
