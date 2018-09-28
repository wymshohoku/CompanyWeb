# coding=utf-8

from bottle import get, put
from common import web_helper, string_helper, db_helper
from config import db_config

@get('/api/about/')
def callback():
    """
    获取指定记录
    """
    sql = """select * from infomation where id = 1"""
    # 读取记录
    with db_helper.PgHelper(db_config.DB, db_config.IS_OUTPUT_SQL) as db:
        result = db.execute(sql)
    if result:
        # 直接输出json
        return web_helper.return_msg(0, '成功', result[0])
    else:
        return web_helper.return_msg(-1, "查询失败")


@put('/api/about/')
def callback1():
    """
    修改记录
    """
    front_cover_img = web_helper.get_form('front_cover_img', '图片')
    content = web_helper.get_form('content', '内容', is_check_special_char=False)
    # 防sql注入攻击处理
    content = string_helper.filter_str(content, "'")
    # 防xss攻击处理
    content = string_helper.clear_xss(content)

    # 更新记录
    sql = """update infomation set front_cover_img=%s, content=%s where id=1"""
    vars = (front_cover_img, content,)
    # 写入数据库
    with db_helper.PgHelper(db_config.DB, db_config.IS_OUTPUT_SQL) as db:
        db.execute(sql, vars)
        db.commit()

    # 直接输出json
    return web_helper.return_msg(0, '成功')