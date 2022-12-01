import numpy as np


def get_row_column_neighbour(cell_id):
    return [
        (cell_id[0], cell_id[1] - 1),
        (cell_id[0], cell_id[1] + 1),
        (cell_id[0] - 1, cell_id[1]),
        (cell_id[0] + 1, cell_id[1]),
    ]


def mark_unique(cell_id):
    if (value_array[cell_id[0], ...].tolist().count(value_array[cell_id]) == 1) and (
            value_array[..., cell_id[1]].tolist().count(value_array[cell_id]) == 1):
        mark_array[cell_id] = 'circle'


def is_border_cell(cell_id):
    return cell_id[0] == 0 or cell_id[1] == 0 or cell_id[0] == row_count - 1 or cell_id[1] == column_count - 1


def id_exists(cell_id):
    return 0 <= cell_id[0] < row_count and 0 <= cell_id[1] < column_count


def get_diagonal_neighbour(cell_id, mark_array_copy, only_dark=False):
    all_diagonal_id = [(cell_id[0] + 1, cell_id[1] - 1), (cell_id[0] + 1, cell_id[1] + 1),
                       (cell_id[0] - 1, cell_id[1] - 1), (cell_id[0] - 1, cell_id[1] + 1)]
    result = []
    for _id in all_diagonal_id:
        if id_exists(_id):
            if only_dark:
                if mark_array_copy[_id] == 'dark':
                    result.append(_id)
            else:
                result.append(_id)
    return result


def mark_circle(cell_id):
    if mark_array[cell_id] != 'blank':
        return None

    mark_array[cell_id] = 'circle'
    circled_value = value_array[cell_id]

    for num in range(column_count):
        id_1 = (cell_id[0], num)
        if mark_array[id_1] == 'blank' and value_array[id_1] == circled_value:
            mark_dark(id_1)

    for num_1 in range(row_count):
        id_2 = (num_1, cell_id[1])
        if mark_array[id_2] == 'blank' and value_array[id_2] == circled_value:
            mark_dark(id_2)


def mark_dark(cell_id):
    if mark_array[cell_id] != 'blank':
        return None

    mark_array[cell_id] = 'dark'

    for _id in get_row_column_neighbour(cell_id):
        if id_exists(_id):
            mark_circle(_id)


def mark_virtual_circle(cell_id):
    if virtual_mark_array[cell_id] != 'blank':
        return None

    virtual_mark_array[cell_id] = 'circle'
    circled_value = value_array[cell_id]

    for num in range(column_count):
        id_1 = (cell_id[0], num)
        if virtual_mark_array[id_1] == 'blank' and value_array[id_1] == circled_value:
            mark_virtual_dark(id_1)

    for num_1 in range(row_count):
        id_2 = (num_1, cell_id[1])
        if virtual_mark_array[id_2] == 'blank' and value_array[id_2] == circled_value:
            mark_virtual_dark(id_2)


def mark_virtual_dark(cell_id):
    if virtual_mark_array[cell_id] != 'blank':
        return None

    virtual_mark_array[cell_id] = 'dark'

    row_column_neighbour = get_row_column_neighbour(cell_id)

    for _id in row_column_neighbour:
        if id_exists(_id):
            mark_virtual_circle(_id)


def virtual_error_occured():
    for _id in all_id_list:
        if loop_form_if_darken(_id, virtual_mark_array) and virtual_mark_array[_id] == 'dark':
            return True

        if virtual_mark_array[_id] == 'dark':
            row_column_neighbour = get_row_column_neighbour(_id)
            for id_ in row_column_neighbour:
                if id_exists(id_) and virtual_mark_array[id_] == 'dark':
                    return True

    for index in range(column_count):
        column_value_array = value_array[..., index]
        column_mark_array = virtual_mark_array[..., index]
        column_circled_values = column_value_array[column_mark_array == 'circle']
        if len(column_circled_values.tolist()) != len(set(column_circled_values.tolist())):
            return True

    for index in range(row_count):
        row_value_array = value_array[index, ...]
        row_mark_array = virtual_mark_array[index, ...]
        row_circled_values = row_value_array[row_mark_array == 'circle']
        if len(row_circled_values.tolist()) != len(set(row_circled_values.tolist())):
            return True


def check_for_dark_advanced(cell_id):
    if mark_array[cell_id] != 'blank':
        return None

    for _id in all_id_list:
        virtual_mark_array[_id] = mark_array[_id]

    mark_virtual_circle(cell_id)

    if virtual_error_occured():
        mark_dark(cell_id)

    for _id in all_id_list:
        if loop_form_if_darken(_id, virtual_mark_array) and virtual_mark_array[_id] == 'blank':
            mark_virtual_circle(_id)

        if virtual_error_occured():
            mark_dark(cell_id)


def check_for_circle_advanced(cell_id):
    if mark_array[cell_id] != 'blank':
        return None

    for _id in all_id_list:
        virtual_mark_array[_id] = mark_array[_id]

    mark_virtual_dark(cell_id)

    if virtual_error_occured():
        mark_circle(cell_id)

    for _id in all_id_list:
        if loop_form_if_darken(_id, virtual_mark_array) and virtual_mark_array[_id] == 'blank':
            mark_virtual_circle(_id)

        if virtual_error_occured():
            mark_circle(cell_id)


def loop_form_if_darken(cell_id, mark_array_copy):
    connected_blacks = [cell_id]
    checked_cells = []
    border_flag = is_border_cell(cell_id)

    while len(connected_blacks) > 0:
        new_black_connections = []
        for black_id in connected_blacks:
            neighbours = get_diagonal_neighbour(black_id, mark_array_copy, True)
            for _id in neighbours:
                if _id not in checked_cells:
                    new_black_connections.append(_id)

        for id_ in new_black_connections:
            if is_border_cell(id_):
                if border_flag:
                    return True
                else:
                    border_flag = True
            if new_black_connections.count(id_) >= 2:
                return True

        checked_cells += connected_blacks
        connected_blacks = new_black_connections
    return False


def take_input():
    with open(input("Введите абсолютный путь до файла с головоломкой: "), 'r') as infile:
        list_data = []

        part = infile.readline()
        while part:
            list_data.append(list(map(int, part.strip().split(','))))
            part = infile.readline()
        infile.close()

    all_value_array = np.array(list_data)
    return all_value_array


def print_solution():
    for sub_list in mark_array:
        for mark in sub_list:
            if mark == 'dark':
                print(' X ', end='')
            elif mark == 'circle':
                print(' O ', end='')
            else:
                print(' ? ', end='')
        print('')





if __name__ == '__main__':
    value_array = take_input()
    try:
        column_count = value_array.shape[1]
    except IndexError:
        print("У головоломки все строчки должны иметь одну длину")
        exit()
    try:
        row_count = value_array.shape[0]
    except IndexError:
        print("У головоломки все столбцы должны иметь одну длину")
        exit()

    print(value_array)

    mark_array = np.array([['blank'] * column_count] * row_count, dtype='<U6')
    virtual_mark_array = np.array(mark_array)
    all_id_list = []
    for i in range(row_count):
        for j in range(column_count):
            all_id_list.append((i, j))

    for i in all_id_list:
        mark_unique(i)
    while True:
        prev_mark_array = np.array(mark_array)
        stop_flag = True
        for i in all_id_list:
            check_for_dark_advanced(i)
        for i in all_id_list:
            check_for_circle_advanced(i)
        for i in all_id_list:
            if prev_mark_array[i] != mark_array[i]:
                stop_flag = False
                break
        if stop_flag:
            break
        if 'blank' not in mark_array.flatten().tolist():
            break

    print_solution()
