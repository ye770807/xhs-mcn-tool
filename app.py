from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# 存储当前查询到的用户信息（简单实现，实际应用应该使用session或数据库）
user_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query_user():
    """查询博主信息"""
    data = request.json
    user_id = data.get('user_id', '').strip()
    
    if not user_id:
        return jsonify({'success': False, 'message': '请输入博主ID'})
    
    try:
        url = f"https://creator.xiaohongshu.com/api/galaxy/sign/user/search?keyword={user_id}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 QQBrowser/21.1.8531.400",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "sec-ch-ua": "\"Chromium\";v=\"123\", \"Not:A-Brand\";v=\"8\"",
            "x-t": "1778828517578",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 QQBrowser/21.1.8531.400",
            "x-b3-traceid": "c0a8117f687d8e4c4e10f4827f3f9f43",
            "sec-fetch-site": "same-origin",
            "x-s": "0Gvj1K0wZmPsT0Li2F5sT0Li2F5sZmPsT0LivF5sT0Li2F5sZmPsT0Li2F5sZmPsT0Li2F5sZmP",
            "x-s-common": "2UQapN9af0yDZn6sT0Li2F5sZmPsT0Li2F5sZmPsT0Li2F5sZmPsT0Li2F5sZmPsT0Li2F5sZmP",
            "sec-fetch-mode": "cors",
            "x-b3-spanid": "c0a8117f687d8e4c",
            "Referer": "https://creator.xiaohongshu.com/",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "acw_tc=0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return jsonify({'success': False, 'message': f'HTTP错误：{response.status_code}'})
        
        result = response.json()
        
        if result.get('code') == 0 and result.get('data'):
            data_field = result.get('data', {})
            if isinstance(data_field, dict) and 'users' in data_field:
                users = data_field.get('users', [])
                if users:
                    user_info = users[0]
                    user_data = {
                        'user_id': user_info.get('userId'),
                        'nickname': user_info.get('nickname'),
                        'fans_count': user_info.get('fansCount'),
                        'avatar': user_info.get('avatar')
                    }
                    return jsonify({
                        'success': True, 
                        'message': '查询成功',
                        'data': user_data
                    })
                else:
                    return jsonify({'success': False, 'message': '未找到该博主信息'})
            else:
                return jsonify({'success': False, 'message': '数据格式错误'})
        else:
            return jsonify({'success': False, 'message': '未找到该博主信息'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'查询失败：{str(e)}'})

@app.route('/api/attach', methods=['POST'])
def attach_user():
    """挂靠博主"""
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name', '').strip()
    area_code = data.get('area_code', '')
    phone_number = data.get('phone_number', '').strip()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    if not user_id:
        return jsonify({'success': False, 'message': '请先查询博主信息'})
    
    if not name:
        return jsonify({'success': False, 'message': '请输入姓名'})
    
    if not phone_number:
        return jsonify({'success': False, 'message': '请输入电话号码'})
    
    try:
        url = "https://creator.xiaohongshu.com/api/galaxy/sign/anchor/invite"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 QQBrowser/21.1.8531.400",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json;charset=UTF-8",
            "sec-ch-ua": "\"Chromium\";v=\"123\", \"Not:A-Brand\";v=\"8\"",
            "x-t": "1778828517578",
            "sec-ch-ua-mobile": "?0",
            "x-b3-traceid": "c0a8117f687d8e4c4e10f4827f3f9f43",
            "sec-fetch-site": "same-origin",
            "x-s": "0Gvj1K0wZmPsT0Li2F5sT0Li2F5sZmPsT0LivF5sT0Li2F5sZmPsT0Li2F5sZmPsT0Li2F5sZmP",
            "x-s-common": "2UQapN9af0yDZn6sT0Li2F5sZmPsT0Li2F5sZmPsT0Li2F5sZmPsT0Li2F5sZmPsT0Li2F5sZmP",
            "sec-fetch-mode": "cors",
            "x-b3-spanid": "c0a8117f687d8e4c",
            "Referer": "https://creator.xiaohongshu.com/",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "acw_tc=0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a"
        }
        
        # 转换日期为时间戳
        start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
        end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp() * 1000)
        
        payload = {
            "userId": user_id,
            "name": name,
            "areaCode": area_code,
            "phoneNumber": phone_number,
            "startTime": start_timestamp,
            "endTime": end_timestamp
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code != 200:
            return jsonify({'success': False, 'message': f'HTTP错误：{response.status_code}'})
        
        result = response.json()
        
        if result.get('code') == 0 or result.get('success') == True:
            return jsonify({'success': True, 'message': '挂靠成功'})
        else:
            error_msg = result.get('msg', '')
            if '用户手机号填写错误' in error_msg:
                return jsonify({'success': False, 'message': '手机号错误请检查'})
            elif '与博主真实姓名不符' in error_msg:
                return jsonify({'success': False, 'message': '姓名错误请检查'})
            else:
                return jsonify({'success': False, 'message': '挂靠失败'})
                
    except Exception as e:
        return jsonify({'success': False, 'message': f'挂靠失败：{str(e)}'})

if __name__ == '__main__':
    # 允许局域网访问，方便手机连接
    app.run(host='0.0.0.0', port=5000, debug=True)
