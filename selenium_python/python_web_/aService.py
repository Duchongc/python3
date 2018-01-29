import pymysql
from builtins import int

#xie chu han shu
def connDB():#lain jie shu ju ku
    conn = pymysql.Connect("120.92.79.213", "duchongchong", "AB1.2.3.", "test")
    cur = conn.cursor()
    return (conn,cur)

def exeUpdate(conn,cur,sql):#geng xin huo cha ru
    sta = cur.execute(sql)
    conn.commit()
    return (sta)

def exeDelet(conn,cur,IDs):#shan chu4\


    for id in IDs:
        sta = cur.execute("delete from test where id = %d" %(int(id)))
    conn.commit()
    return (sta)

def exeQuery(cur,sql):#cha xun
    cur.execute(sql)
    return (cur)

def connClose(conn,cur):#guan bi
    cur.close()
    conn.close()

result = True

conn,cur=connDB()




while (result):
        print("请选择以上四个操作：1，修改记录，2,，增加记录，3，查询记录，4，删除记录")
        number = input()
        if (number == 'q'):
            print("结束操作")
            break
        elif (int(number) == 1):
            sql = input("请输入更新语句")
            try:
                exeUpdate(conn, cur, sql)
                print("更新成功")

            except Exception:
                print("更新失败")
                raise
        elif (int(number) == 2):
            sql = input("请输入新增语句")
            try:
                exeUpdate(conn, cur, sql)
                print("更新成功")
                break
            except Exception:
                print("更新失败")
                raise
        elif (int(number) == 3):
            sql = input("请输入查询语句")
            try:
                exeQuery(cur, sql)
                for item in cur:
                    print("ID=" + str(item[0]) + "name=" + item[1])
                print("查询成功")

            except Exception:
                print("查询失败")
                raise
        elif (int(number) == 4):
            ids = input("请输入id,并用空格隔开")
            try:
                exeDelet(conn, cur, ids)
                print("删除成功")

            except Exception:
                print("删除失败")
                raise
        else:
            print("非法输入，将结束操作")
            result = False
            break




'''
class AService(object):
    def lianjie():
        conn = pymysql.connect(
            "localhost",
            "root",
            "root",
            "test"

        )
        cursor = conn.cursor()
        cursor.execute("select * from test")
        reselt = cursor.fetchall()#展示查询的所有数据
        i = []
        for i in reselt:#放入i集合遍历
          print(i)
        cursor.close()
        conn.close()
        return reselt
    def select():
        sql = "INSERT INTO test  VALUES(null,'杨梦林','111','12345678','12345678@qq.com','鬼子','25','178','火星')"
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


AService.lianjie()'''
