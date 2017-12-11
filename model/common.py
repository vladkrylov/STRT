def filter_by_id(sequence, item_id):
    res = filter(lambda item: item.id == item_id, sequence)
    if len(res) != 0:
        return res[0]
    return None

