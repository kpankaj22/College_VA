from actions import sql_conn

def query_pd(branch):
    db = sql_conn.create_conn()
    dbcursor=db.cursor()
    query=f"Select prof_name from prof_subject where domain = '{branch}'"
    dbcursor.execute(query)

    pd=dbcursor.fetchall()

    if len(list(pd))==0:
        text = "entered inputs are wrong"
    else:
        text = f"{pd}"

    print(pd)

query_pd("AI")