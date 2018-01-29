import pymysql
sql = "INSERT INTO test  VALUES('4','潇洒哥','110','123456789','123456789@qq.com','中国','30','185','北京市')"
db = pymysql.connect(
    "localhost",
    "root",
    "root",
    "test"

)  # 操作游标
cursor = db.cursor()
try:
    cursor.execute(sql)  # 执行sql
    db.commit()  # 提交到数据库执行

except:
    db.rollback()  # 回滚
cursor.close()
db.close()