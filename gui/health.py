from flask import Blueprint
from core import save_sql
from flask import Flask, render_template, request, jsonify
import requests
# 创建蓝图对象
health_blueprint = Blueprint('health_blueprint', __name__)

# 定义路由和视图函数
@health_blueprint.route('/health/save_heart',methods=['POST'])
def save_heart():
    data = request.get_json()
    save_sql.save_heart_data(data)
    return "Heart data saved successfully"

