import sqlite3
import json
from datetime import datetime
def add_heart_data_table():
    # 连接到数据库（如果数据库不存在，则会自动创建）
    conn = sqlite3.connect('../Ecarebot.db')

    # 创建游标对象
    cursor = conn.cursor()

    # 创建数据表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heart_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state INTEGER,
            meanHR REAL,
            rmssd REAL,
            ANS REAL,
            stressIndex REAL,
            HRs TEXT,
            arrhythmiaNum INTEGER,
            prob_AF REAL,
            prob_PXC REAL,
            prob_N_shape REAL,
            prob_other REAL,
            createdAt TEXT
        )
    ''')

    # # 插入一条数据
    # data = (1, 70, 50, 0.5, 3, 2, 0.8, 0.2, 0.3, 0.5, '2022-02-22 10:00:00')
    # cursor.execute('INSERT INTO health_data (state, meanHR, rmssd, ANS, stressIndex, arrhythmiaNum, prob_AF, prob_PXC, prob_N_shape, prob_other, createdAt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)

    # 提交事务
    conn.commit()

    # 关闭连接
    conn.close()

def save_heart_data(data):
    # 解析返回结果
    result = json.loads(data)
    state = result['data']['state']
    meanHR = result['data']['meanHR']
    rmssd = result['data']['rmssd']
    ANS = result['data']['ANS']
    stressIndex = result['data']['stressIndex']
    HRs = result['data']['HRs']
    arrhythmiaNum = result['data']['arrhythmiaNum']
    prob_AF = result['data']['prob_AF']
    prob_PXC = result['data']['prob_PXC']
    prob_N_shape = result['data']['prob_N_shape']
    prob_other = result['data']['prob_other']
    # 获取当前时间
    current_time = datetime.now()

    # 将时间格式化为字符串
    createdAt = current_time.strftime('%Y-%m-%d %H:%M:%S')

    # 连接到数据库
    conn = sqlite3.connect('../Ecarebot.db')
    cursor = conn.cursor()

    # 插入一条数据
    insert_query = "INSERT INTO health_data (state, meanHR, rmssd, ANS, stressIndex, HRs, arrhythmiaNum, prob_AF, prob_PXC, prob_N_shape, prob_other, createdAt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (state, meanHR, rmssd, ANS, stressIndex, json.dumps(HRs), arrhythmiaNum, prob_AF, prob_PXC, prob_N_shape, prob_other, createdAt)
    cursor.execute(insert_query, values)

    # 提交事务并关闭连接
    conn.commit()
    conn.close()