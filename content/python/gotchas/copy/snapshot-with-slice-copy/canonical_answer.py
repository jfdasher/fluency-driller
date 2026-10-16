def record_snapshots(ops):
    cur = []
    snapshots = []
    for op in ops:
        cur.append(op)
        snapshots.append(cur[:])
    return snapshots
