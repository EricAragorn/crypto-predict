def list_to_string(s):
    """Convert a list to a string delimited by ","

    Args:
        s: the set to convert

    Returns:
        A formatted string
        format:
        FST,SND,TRD,...

    """

    param_string = ''
    count = 0
    for p in s:
        if count != 0:
            param_string += ","
        param_string += p
        count += 1

    return param_string


def string_to_double(s):
    """Convert all string elements in a list to double

    Args:
       s: the set to convert

    Returns:
        A list with all eligible string elements converted to double
    """
    new_list = []
    for p in s:
        v = p
        if type(p) is str:
            try:
                v = float(p)
            except ValueError:
                None
        new_list.append(v)
    return new_list

