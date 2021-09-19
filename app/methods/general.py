def mycursor_to_json(mycursor):
    # creates JSON from sql query
    row_headers = [x[0] for x in mycursor.description]
    sve = mycursor.fetchall()
    if len(sve) == 0:
        return None
    out = []
    for rv in sve:
        dicc = {rowname: rv[rownum]
                for rownum, rowname in enumerate(row_headers)}
        out.append(dicc)
    return out


def sublist(lst1, lst2):
    for i1 in lst1:
        if i1 in lst2:
            ...
        else:
            return False
    return True
