import pyodbc

def connect2Db(server,database,username,password):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';Direct=True;Database='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    return cursor

def getTableNames(cursor):
    
    sqlGetTables="SELECT TABLE_NAME as tablename "
    sqlGetTables+=" FROM INFORMATION_SCHEMA.TABLES "
    sqlGetTables+=" WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='softone' "
    cursor.execute(sqlGetTables) 
    return cursor.fetchall()

def lastTableUpdateDateTime(cursor,tablename,db):
    sql="SELECT OBJECT_NAME(OBJECT_ID) AS tablebaseName, last_user_update as lup,* "
    sql+=" FROM sys.dm_db_index_usage_stats "
    sql+=" WHERE database_id = DB_ID('"+db+"') "
    sql+=" AND OBJECT_ID=OBJECT_ID('"+tablename+"') "
    
    
    cursor.execute(sql) 
    return cursor.fetchone()
    
SERVER ="..."
DB="..."
USERNAME="..."
PASSWORD="..."


cursor = connect2Db(SERVER,DB,USERNAME,PASSWORD)

tables = getTableNames(cursor)
for table in tables:
    lastUpdate = lastTableUpdateDateTime(cursor,table.tablename,DB)
    if lastUpdate and lastUpdate.lup:
        print(table.tablename)
        print(lastUpdate.lup)
