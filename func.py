def remove_tuple(t):
    return str(t[0])

def fetch_amount(cur, count):
    return list(map(remove_tuple, cur.fetchmany(count)))
