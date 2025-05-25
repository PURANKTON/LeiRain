import pymysql
import random
import os


class HitokotoSystem:
    def __init__(self, host='localhost', user='root', password='', database='hitokoto', charset='utf8mb4'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self._init_database()

    def _get_connection(self):
        """获取数据库连接"""
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset,
            cursorclass=pymysql.cursors.DictCursor
        )

    def _init_database(self):
        """初始化数据库和表结构"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    # 创建表
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS hitokoto (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        content TEXT NOT NULL,
                        author VARCHAR(255),
                        source VARCHAR(255),
                        category VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                    ''')
                conn.commit()
        except pymysql.Error as e:
            print(f"数据库初始化失败: {e}")

    def add_hitokoto(self, content, author=None, source=None, category=None):
        """添加一条新的一言"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = '''
                    INSERT INTO hitokoto (content, author, source, category) 
                    VALUES (%s, %s, %s, %s)
                    '''
                    cursor.execute(sql, (content, author, source, category))
                conn.commit()
                return cursor.lastrowid
        except pymysql.Error as e:
            print(f"添加一言失败: {e}")
            return None

    def get_random_hitokoto(self, category=None):
        """获取随机一言，可指定分类"""
        sql = 'SELECT * FROM hitokoto'
        params = []
        if category:
            sql += ' WHERE category = %s'
            params.append(category)
        sql += ' ORDER BY RAND() LIMIT 1'

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()

    def get_hitokoto_by_id(self, hitokoto_id):
        """根据ID获取一言"""
        sql = 'SELECT * FROM hitokoto WHERE id = %s'

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (hitokoto_id,))
                return cursor.fetchone()

    def update_hitokoto(self, hitokoto_id, content=None, author=None, source=None, category=None):
        """更新一言内容"""
        update_fields = []
        params = []

        if content is not None:
            update_fields.append('content = %s')
            params.append(content)
        if author is not None:
            update_fields.append('author = %s')
            params.append(author)
        if source is not None:
            update_fields.append('source = %s')
            params.append(source)
        if category is not None:
            update_fields.append('category = %s')
            params.append(category)

        if not update_fields:
            return False

        params.append(hitokoto_id)
        update_query = ', '.join(update_fields)
        sql = f'UPDATE hitokoto SET {update_query} WHERE id = %s'

        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                conn.commit()
                return cursor.rowcount > 0
        except pymysql.Error as e:
            print(f"更新一言失败: {e}")
            return False

    def delete_hitokoto(self, hitokoto_id):
        """删除一言"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = 'DELETE FROM hitokoto WHERE id = %s'
                    cursor.execute(sql, (hitokoto_id,))
                conn.commit()
                return cursor.rowcount > 0
        except pymysql.Error as e:
            print(f"删除一言失败: {e}")
            return False

    def list_hitokoto(self, limit=10, offset=0, category=None):
        """获取一言列表，支持分页和分类筛选"""
        sql = 'SELECT * FROM hitokoto'
        params = []
        if category:
            sql += ' WHERE category = %s'
            params.append(category)
        sql += ' ORDER BY created_at DESC LIMIT %s OFFSET %s'
        params.extend([limit, offset])

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()

    def get_categories(self):
        """获取所有分类列表"""
        sql = 'SELECT DISTINCT category FROM hitokoto WHERE category IS NOT NULL'

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return [row['category'] for row in cursor.fetchall()]

    def count_hitokoto(self, category=None):
        """统计一言数量，可按分类统计"""
        sql = 'SELECT COUNT(*) as count FROM hitokoto'
        params = []
        if category:
            sql += ' WHERE category = %s'
            params.append(category)

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()['count']


# 示例使用
if __name__ == "__main__":
    # 初始化一言系统，请修改为你的MySQL连接信息
    hitokoto = HitokotoSystem(
        host='192.168.10.105',
        user='tangrain',
        password='LTNmsn74ytJdYYEi',
        database='tangrain'
    )

    # # 添加一些示例一言
    # hitokoto.add_hitokoto(
    #     content="人生就像骑自行车，要想保持平衡就得往前走。",
    #     author="爱因斯坦",
    #     source="名言",
    #     category="励志"
    # )
    # hitokoto.add_hitokoto(
    #     content="世界上只有一种真正的英雄主义，那就是在认清生活的真相后依然热爱它。",
    #     author="罗曼·罗兰",
    #     source="《约翰·克利斯朵夫》",
    #     category="哲理"
    # )

    # 获取随机一言
    random_hitokoto = hitokoto.get_random_hitokoto()
    print("随机一言:", random_hitokoto)

    # 获取所有分类
    categories = hitokoto.get_categories()
    print("分类列表:", categories)