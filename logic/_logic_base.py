# coding=utf-8

from common import db_helper


class LogicBase():
    """逻辑层基础类"""

    def __init__(self, db, is_output_sql, table_name, column_name_list='*', pk_name='id'):
        """类初始化"""
        # 数据库参数
        self.__db = db
        # 是否输出执行的Sql语句到日志中
        self.__is_output_sql = is_output_sql
        # 表名称
        self.__table_name = str(table_name).lower()
        # 查询的列字段名称，*表示查询全部字段，多于1个字段时用逗号进行分隔，除了字段名外，也可以是表达式
        self.__column_name_list = str(column_name_list).lower()
        # 主健名称
        self.__pk_name = str(pk_name).lower()

    #####################################################################
    ### 执行Sql ###

    def get_model(self, wheres):
        """通过条件获取一条记录"""
        # 如果有条件，则自动添加where
        if wheres:
            wheres = ' where ' + wheres

        # 合成sql语句
        sql = "select %(column_name_list)s from %(table_name)s %(wheres)s" % \
              {'column_name_list': self.__column_name_list, 'table_name': self.__table_name, 'wheres': wheres}
        # 初化化数据库链接
        result = self.select(sql)
        if result:
            return result[0]
        return {}

    def get_model_for_pk(self, pk, wheres=''):
        """通过主键值获取数据库记录实体"""
        if not pk:
            return {}
        # 组装查询条件
        wheres = '%s = %s' % (self.__pk_name, str(pk))

        return self.get_model(wheres)

    def add_model(self, fields, returning=''):
        """新增数据库记录"""
        ### 拼接sql语句 ###
        # 初始化变量
        key_list = []
        value_list = []
        # 将传入的字典参数进行处理，把字段名生成sql插入字段名数组和字典替换数组
        # PS:字符串使用字典替换参数时，格式是%(name)s，这里会生成对应的字串
        # 比如：
        #   传入的字典为： {'id': 1, 'name': '名称'}
        #   那么生成的key_list为：'id','name'
        #   而value_list为：'%(id)s,%(name)s'
        #   最终而value_list为字符串对应名称位置会被替换成相应的值
        for key in fields.keys():
            key_list.append(key)
            value_list.append('%(' + key + ')s')
        # 设置sql拼接字典，并将数组（lit）使用join方式进行拼接，生成用逗号分隔的字符串
        parameter = {
            'table_name': self.__table_name,
            'pk_name': self.__pk_name,
            'key_list': ','.join(key_list),
            'value_list': ','.join(value_list)
        }
        # 如果有指定返回参数，则添加
        if returning:
            parameter['returning'] = ', ' + returning
        else:
            parameter['returning'] = ''

        # 生成可以使用字典替换的字符串
        sql = "insert into %(table_name)s (%(key_list)s) values (%(value_list)s) returning %(pk_name)s %(returning)s" % parameter
        # 将生成好的字符串替字典参数值，生成最终可执行的sql语句
        sql = sql % fields

        result = self.execute(sql)
        if result:
            return result[0]
        return {}

    def select(self, sql):
        """执行sql查询语句（select）"""
        with db_helper.PgHelper(self.__db, self.__is_output_sql) as db:
            # 执行sql语句
            result = db.execute(sql)
            if not result:
                result = []
        return result

    def execute(self, sql):
        """执行sql语句，并提交事务"""
        with db_helper.PgHelper(self.__db, self.__is_output_sql) as db:
            # 执行sql语句
            result = db.execute(sql)
            if result:
                db.commit()
            else:
                result = []
        return result

    #####################################################################