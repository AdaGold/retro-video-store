def missing_any(request_dict, check_if_missing):
    for i in check_if_missing:
        if i not in request_dict:
            return True
    return False