from flask import Flask
import pymysql
import json

app = Flask(__name__)

# 配置 MySQL 连接信息
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE'] = 'fit5120'

# 数据库连接函数
def get_db_connection():
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )
    return connection

@app.route('/')
def home():
    return "欢迎使用 Flask！"

@app.route('/test-db')
def test_db():
    try:
        # 获取数据库连接
        connection = get_db_connection()
        
        # 执行查询，获取 cancer_mortality 表的所有数据
        with connection.cursor() as cursor:
            cursor.execute("SELECT `year`, SUM(`count`) AS `total_cancer_cases` FROM `cancer_incidence` WHERE `state` = 'Victoria' GROUP BY `year` ORDER BY `year`;")
            result = cursor.fetchall()  # 获取所有记录
        
        # 关闭数据库连接
        connection.close()

        # 返回查询结果
        if result:
            # 将结果转换为 JSON 格式以方便查看
            return json.dumps(result, default=str)  # 处理日期等类型转换
        else:
            return "没有查询到数据"
    
    except Exception as e:
        # 处理数据库连接错误
        return f"数据库连接失败: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
