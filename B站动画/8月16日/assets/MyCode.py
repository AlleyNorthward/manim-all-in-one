def find_remaining_per(origin_list:list, result_list:list, excessive_list: list):
    if len(origin_list) == 0:
        result_list.append(excessive_list.copy())
        return 
    
    for data in origin_list:
        temp_list = origin_list.copy()
        temp_list.remove(data)
        excessive_list.append(data)
        find_remaining_per(temp_list,result_list, excessive_list)
        excessive_list.remove(data)
    return result_list

