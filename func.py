# Haalt een waarde uit een tuple met lengte 1.
def remove_tuple(t):
    return str(t[0])

# Fetch een aantal producten met cursor naar list.
def fetch_amount(cur, count):
    return list(map(remove_tuple, cur.fetchmany(count)))
