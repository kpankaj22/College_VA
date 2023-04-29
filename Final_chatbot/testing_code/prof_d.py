from actions import sql_conn


def query_tt(branch,sem,division):
    db= sql_conn.create_conn()
    dbcursor=db.cursor()
    query=f"Select prof_name,lecture,block,block_number,BATCH From time_table Where branch='{branch}' and sem='{sem}' and division='{division}' and day='{day}' and time >= '{tt_time}' LIMIT 5"
    dbcursor.execute(query)

    tt=dbcursor.fetchone()
    
    if len(list(tt))==0:
        print("entered inputs are wrong")

    print( f"{tt}")
    result=f"Professor {tt[0]} is teaching {tt[1]} subject in block {tt[2]}{tt[3]} "
    print(type(result))
    return result