from typing import Any, List


def quickSort(array: List[Any]) -> List[Any]:
    """Quick sort algorithm.

    Args:
        array (List[Any]): Array to sort.

    Returns:
        List[Any]: Sorted array.
    """
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


def sort_with_reference(
    items: List[Any], reference: List[Any], presorted: bool = False
) -> List[Any]:
    """Sort items based on a reference list.

    Args:
        items (List[Any]): Items to sort.
        reference (List[Any]): Reference list.
        presorted (bool, optional): Whether the reference list is presorted. Defaults to False.

    Returns:
        List[Any]: Sorted items.
    """
    if not presorted:
        sorted_reference = quickSort(reference.copy())
    else:
        sorted_reference = reference

    sorted_items = ["filler"] * len(items)
    for obj, column_value in zip(items, reference):
        ind = sorted_reference.index(column_value)
        sorted_items[ind] = obj

    return sorted_items
