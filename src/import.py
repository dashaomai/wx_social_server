# -*- coding:utf-8 -*-
'''
Created on 2017年7月18日

@author: bmwangz
'''
import json
import time
import pymysql
import datetime

def store(file_name,data):
    with open(file_name, 'w') as json_file:
        json_file.write(json.dumps(data))

def load(file_name):
    with open(file_name,'r',encoding='utf-8') as json_file: # file_name='data.json'
        data = json.load(json_file)
        return data

def timestamp2datetime(timestamp, convert_to_local=False):
    ''' Converts UNIX timestamp to a datetime object. '''
    if isinstance(timestamp, (int, float)):
        dt = datetime.datetime.utcfromtimestamp(timestamp)
        return dt
    if convert_to_local: # 是否转化为本地时间
        dt = dt + datetime.timedelta(hours=8) # 中国默认时区
        return dt
    return timestamp

class MySQL:
    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    # 数据库初始化
    def _init_(self, ip, username, pwd, schema):
        try:
            self.db = pymysql.connect(ip, username, pwd, schema, use_unicode=True, charset="utf8mb4")
            print(self.getCurrentTime(), u"MySQL DB Connect Success")
            self.cur = self.db.cursor()
        except pymysql.Error as e:
            print(self.getCurrentTime(), u"MySQL DB Connect Error :%d: %s" % (e.args[0], e.args[1]))
    # 插入数据
    def insertData(self, table, my_dict):
        try:
            cols = ', '.join(my_dict.keys())
            values = "','".join([item.replace(r"'", "\"") for item in my_dict.values()])
            sql = "replace INTO %s (%s) VALUES (%s)" % (table, cols, "'" + values + "'")
            try:
                result = self.cur.execute(sql)
                insert_id = self.db.insert_id()
                self.db.commit()
                # 判断是否执行成功
                if result:
                    return insert_id
                else:
                    return 0
            except pymysql.Error as e:
                # 发生错误时回滚
                print(sql)
                self.db.rollback()
                print(self.getCurrentTime(), u"Data Insert Failed: %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print(self.getCurrentTime(), u"MySQLdb Error:%d: %s" % (e.args[0], e.args[1]))

def safe(s):
    return pymysql.escape_string(s)

def get_insert_sql(table, dict):
    '''
    生成insert的sql语句
    @table，插入记录的表名
    @dict,插入的数据，字典
    '''
    sql = 'insert into %s set ' % table
    sql += dict_2_str(dict)
    return sql

def get_select_sql(table, keys, conditions, isdistinct=0):
    '''
        生成select的sql语句
    @table，查询记录的表名
    @key，需要查询的字段
    @conditions,插入的数据，字典
    @isdistinct,查询的数据是否不重复
    '''
    if isdistinct:
        sql = 'select distinct %s ' % ",".join(keys)
    else:
        sql = 'select  %s ' % ",".join(keys)
    sql += ' from %s ' % table
    if conditions:
        sql += ' where %s ' % dict_2_str_and(conditions)
    return sql

def get_update_sql(table, value, conditions):
    '''
        生成update的sql语句
    @table，查询记录的表名
    @value，dict,需要更新的字段
    @conditions,插入的数据，字典
    '''
    sql = 'update %s set ' % table
    sql += dict_2_str(value)
    if conditions:
        sql += ' where %s ' % dict_2_str_and(conditions)
    return sql

def get_ddelete_sql(table, conditions):
    '''
        生成detele的sql语句
    @table，查询记录的表名

    @conditions,插入的数据，字典
    '''
    sql = 'delete from  %s  ' % table
    if conditions:
        sql += ' where %s ' % dict_2_str_and(conditions)
    return sql

def dict_2_str(dictin):
    '''
    将字典变成，key='value',key='value' 的形式
    '''
    tmplist = []
    for k, v in dictin.items():
        tmp = "%s='%s'" % (str(k), safe(str(v)))
        tmplist.append(' ' + tmp + ' ')
    return ','.join(tmplist)

def dict_2_str_and(dictin):
    '''
    将字典变成，key='value' and key='value'的形式
    '''
    tmplist = []
    for k, v in dictin.items():
        tmp = "%s='%s'" % (str(k), safe(str(v)))
        tmplist.append(' ' + tmp + ' ')
    return ' AND '.join(tmplist)

def main():
    global mySQL, start_page, end_page, sleep_time, isproxy, proxy, header
    mySQL = MySQL()
    mySQL._init_('127.0.0.1', 'root', '123321' ,'sns_test')

    json_data = load('exported_sns.json')
    for sns in json_data:
        media_list = sns.pop('mediaList')
        if len(media_list) > 0:
            for media in media_list:
                row = {"snsId":sns["snsId"]}
                row["url"] = media
                #print(row)
                mySQL.insertData('media_list', row)
        sns_comments = sns.pop("comments")
        if len(sns_comments) > 0:
            for comments in sns_comments:
                comments["snsId"] = sns["snsId"]
                comments["isCurrentUser"] = '1' if comments["isCurrentUser"] else '0'
                #print(comments)
                mySQL.insertData('sns_comments', comments)
        sns_likes = sns.pop("likes")
        if len(sns_likes) > 0:
            for likes in sns_likes:
                likes["snsId"] = sns["snsId"]
                likes["isCurrentUser"] = '1' if likes["isCurrentUser"] else '0'
                #print(likes)
                mySQL.insertData('sns_likes', likes)
        sns["isCurrentUser"] = '1' if sns["isCurrentUser"] else '0'
        sns["timestamp"] = str(timestamp2datetime(sns["timestamp"]))
        #print(sns)
        mySQL.insertData('main_data', sns)

    print("Done.")

if __name__ == "__main__":
    main()
