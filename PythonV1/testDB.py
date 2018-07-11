import pymysql

conn = pymysql.connect(host = 'server2.sib-host.ru',
                       port = 3306,
                       user = 'sante205',
                       passwd = 'bZrH20dBql',
                       db = 'ads',
                       charset = 'utf8',
                       init_command = 'SET NAMES UTF8'
                       )
cursor = conn.cursor()
cursor.execute("select db_name()")
row = cursor.fetchall()
conn.close()

print("cursor: " + cursor)
print("conn: " + conn)
print("row: " + row)
