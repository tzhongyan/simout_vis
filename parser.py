import pandas as pd

def read_nml(file_path):
    # Read from file path
    try:
        with open(file_path) as f:
            content = [l.strip() for l in f]
    except FileNotFoundError:
        raise Exception('File not found in path.')
    
    # We need to strip the namespace and file ending \ marker
    # So remove first and last item from content
    content = content[1:-1]
    
    # Store items in dictionary
    dic = {}
    this_key = None
    for line in content:
        eq_sp = line.split('=') # split by '='
        nums = None
        if len(eq_sp) > 1: 
            # if there is '=', renew key
            # assume first line starts with key, since we stripped namespace
            this_key = eq_sp[0].strip()
            dic[this_key] = []
            # obtain numbers in string form
            nums = eq_sp[1]
        else:
            # obtain numbers in string form
            nums = eq_sp[0]
        # split the string with ',' to get individual numbers
        nums = nums.split(',')
        # push it into the key as string
        dic[this_key].extend([n.strip() for n in nums])

    # As there would be empty strings because last line in nml we dealing with
    # always comes with a trailing ',' we need to remove them
    # remove empty strings.
    #
    # Also, '*' means multiple items of the same value, we should expand that
    for k, v in dic.items():
        # remove string
        dic[k] = [x for x in dic[k] if x ]
        # detect * to expand
        for n, item in enumerate(dic[k]):
            p_i = item.split('*')
            if len(p_i) > 1:
                # If the string contains *, we should expand it and 
                # set it at place
                temp_l = []
                temp_l.append(p_i[1])
                dic[k][n] = temp_l * int(p_i[0])
    
        # Then we need to flatten the list
        dic[k] = tzy_flatten(dic[k])
    
    return dic

def tzy_flatten(ll):
    """
    Own flatten just for use of this context.
    Expected outcome:
        > flatten([1, 2, [3, 4], [5]])
        [1, 2, 3, 4, 5]
    Only goes 1 depth so should be O(n) time, but also O(n) space
    """
    ret = []
    for item in ll:
        if isinstance(item, list):
            for subitem in item:
                ret.append(subitem)
        else:
            ret.append(item)
    
    return ret

    