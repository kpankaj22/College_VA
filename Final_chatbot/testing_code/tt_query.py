import sql_conn
import da_ti

def query_tt(branch,sem,division):
    db= sql_conn.create_conn()
    dbcursor=db.cursor()
    tt_time=da_ti.current_time()
    if tt_time>16:
        day=da_ti.day_tommorrow()
    elif tt_time<9:
        tt_time=9

    if tt_time>=17 or tt_time<8:
        tt_time= 9
    query=f"Select prof_name,lecture,block,block_number,BATCH From time_table Where branch='{branch}' and sem='{sem}' and division='{division}' and day='{day}' and time >= {tt_time} LIMIT 5"
    dbcursor.execute(query)

    tt=dbcursor.fetchall()
    print(branch,sem,division,day,tt)
    print( f"{tt}")
    result=""
    for row in tt:
        result=result + f"Professor {row[0]} is teaching {row[1]} subject in block {row[2]}{row[3]} for Batch {row[4]}\n"
    
    return result
 

