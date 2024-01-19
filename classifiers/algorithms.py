def count_collab_parameter(params_list, features_list):
    sum = 0
    for index in range(len(params_list) - 1, 0, -1):
        if index != 0:
            sum += (params_list[index] * features_list[index - 1])
        else:
            sum += params_list[0]
    return sum