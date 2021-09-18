def mycursor_to_json(mycursor):
	#creates JSON from sql query
	row_headers=[x[0] for x in mycursor.description]
	sve = mycursor.fetchall()
	if len(sve) == 0:
		return None
	out = []
	for rv in sve: 
		dicc = {}
		for rownum, rowname in enumerate(row_headers):
			dicc[rowname] = rv[rownum]
		out.append(dicc)
	return out