def search(number: id, array: list) -> bool:
    left = 0
    right = len(array) - 1

    while left <= right:
        mid = (left + right) // 2
        if array[mid] == number:
            return True
        elif array[mid] > number:
            right = mid - 1
        elif array[mid] < number:
            left = mid + 1
    return False


if __name__ == "__main__":
    array = [1, 2, 3, 45, 356, 569, 600, 705, 923]
    print(search(666, array))
