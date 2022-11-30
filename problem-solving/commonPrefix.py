def commonPrefix(string_array):
    integer_array= []

    for string in string_array:
        split_strings = [[string[:index], string[index:]] for index in range(len(string))]

        for split_string in split_strings:
            if string.startswith(split_string[1]):
                common_prefix = split_string[1]
                integer_array.append(len(common_prefix))
            else:
                possible_common_prefix= [split_string[1][:index] for index in range(len(split_string[1])) if string.startswith(split_string[1][:index])]
                common_prefix = len(possible_common_prefix[-1])
                integer_array.append(common_prefix)

    sum = 0
    for i in integer_array: 
        sum += i

    return sum