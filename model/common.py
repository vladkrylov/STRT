def filter_by_id(sequence, item_id):
    res = filter(lambda item: item.id == item_id, sequence)
    if len(res) != 0:
        return res[0]
    return None

def generate_run_id(existing_runs):
    if len(existing_runs) == 0:
        run_id = 0
    else:
        run_id = max([run.id for run in self.runs]) + 1
    return run_id 
