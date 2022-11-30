# 2 - Common Prefix Length

Given a string, split the string into two substrings at every possible point. The rightmost substring is a suffix. The beginning of the string is the prefix. Determine the lengths of the common prefix between each suffix and the original string. Sum and return the lengths of the common prefixes. Return an array where each element i is the sum for string `i`.

Example

Consider the only string in the array inputs = `['abcabcd']`. Each suffix is compared to the original string

| Remove to leave Suffix | Suffix    | Common Prefix | Length |
|------------------------|-----------|---------------|--------|
| ''                     | 'abcabcd' | 'abcabcd'     | 7      |
| 'a'                    | 'bcabcd'  | ''            | 0      |
| 'ab'                   | 'cabdc'   | ''            | 0      |
| 'abc'                  | 'abcd'    | 'abc'         | 3      |
| 'abca'                 | 'bcd'     | ''            | 0      |
| 'abcab'                | 'cd'      | ''            | 0      |
| 'abcabc'               | 'd'       | ''            | 0      |


```
The sum is 7 + 0 + 0 + 3 + 0 + 0 + 0 = 10.
```

## Function Description
Complete the function commonPrefix as presented below:

```python
# Complete the 'commonPrefix' function below.
# The function is expected to return an INTEGER_ARRAY.
# The function accepts STRING_ARRAY inputs as parameter.

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
```

