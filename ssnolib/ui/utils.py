def remove_off_after_on(input_list):
    """
    Remove "off" after "on" in the input list
    """
    result = []
    skip_next = False  # Flag to skip the next item if it is an "off" after "on"

    for i in range(len(input_list)):
        if skip_next:
            skip_next = False  # Reset the flag and skip this iteration
            continue

        if input_list[i] == "on":
            result.append("on")
            # Set flag to skip the next element, since it will be "off"
            skip_next = True
        else:
            result.append(input_list[i])

    return result
