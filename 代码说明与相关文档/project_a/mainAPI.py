import re
import requests
import os
import json
import time
from snownlpModified import SnowNLP
from flask_cors import *
from flask import Flask, render_template, request, Response
from shieldWords import shield_sensitive_word as s
import generateVectorData as gv
import ModelApplication
import CompareAnalysis
import conf
import threading
from datetime import datetime
import traceback
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from llmService import llm_service

try:
    from coldModel import calculate_bully_level_v2, get_model_status
    USE_COLD = True
except Exception as e:
    print(f"COLD 模型导入失败，使用原有算法: {e}")
    USE_COLD = False

app = Flask(__name__)
CORS(app, supports_credentials=True)
# 限流器
limiter = Limiter(get_remote_address, app=app)

# 【核心修改】将列表改为字典，实现多房间隔离
# 数据结构: {"房间号": ["时间*昵称*文本*文本", ...]}
bullets_dict = {}

def get_room_bullets(roomid):
    """辅助函数：获取指定房间的弹幕列表，如果没有则初始化为空列表"""
    if not roomid:
        return []
    if roomid not in bullets_dict:
        bullets_dict[roomid] = []
    return bullets_dict[roomid]


# ==========================================
# 智能分级算法：网络欺凌4级评估
# ==========================================
BULLY_WORDS = ['死', '滚', '傻', '垃圾', '脑残', '废物', '恶心', '丑', '婊', '贱', '爹', '妈', '狗', '智障']

def calculate_bully_level_legacy(text, sentiment_score):
    """原有算法：按情感分值、欺凌词密度、语气强度自动分级（降级使用）"""
    length = len(text) if len(text) > 0 else 1
    
    # 1. 欺凌词密度计算
    bully_count = sum(1 for word in BULLY_WORDS if word in text)
    density = bully_count / length
    
    # 2. 语气强度计算
    tone_intensity = text.count('！') + text.count('!') + text.count('？') + text.count('?')
    
    # 3. 自动分级判定
    if sentiment_score < -0.8 or density > 0.3 or (bully_count >= 2 and tone_intensity >= 2):
        return {"level": 4, "levelName": "高危", "action": "拦截 + 预警上报", "color": "#f87171", "method": "legacy"}
    elif sentiment_score < -0.5 or density > 0.15 or bully_count >= 1:
        return {"level": 3, "levelName": "重度", "action": "警告并折叠", "color": "#fb923c", "method": "legacy"}
    elif sentiment_score < -0.2 or tone_intensity >= 3:
        return {"level": 2, "levelName": "中度", "action": "警告提示", "color": "#fbbf24", "method": "legacy"}
    elif sentiment_score < 0:
        return {"level": 1, "levelName": "轻度", "action": "善意提醒", "color": "#60a5fa", "method": "legacy"}
    else:
        return {"level": 0, "levelName": "常规", "action": "正常放行", "color": "#34d399", "method": "legacy"}

def calculate_bully_level(text, sentiment_score):
    """新算法：优先使用 COLD 模型理解上下文，失败则降级使用原有算法"""
    if USE_COLD:
        try:
            cold_result = calculate_bully_level_v2(text)
            if cold_result is not None:
                return cold_result
        except Exception as e:
            print(f"COLD 模型分析失败，降级使用原有算法: {e}")
    
    return calculate_bully_level_legacy(text, sentiment_score)


# ==========================================
# 路由与 API 接口
# ==========================================

@app.route('/')
def index():
    model_info = {
        'available': False,
        'model': 'legacy'
    }
    try:
        from coldModel import get_model_status
        model_info = get_model_status()
    except:
        pass
    
    return Response(json.dumps({
        'status': 'ok',
        'message': '弹幕智能预警系统 API 服务运行中',
        'version': 'v3.0 COLD',
        'model': model_info,
        'endpoints': {
            'B站弹幕': '/getBulletScreen?roomid=房间号',
            '情感分析': '/CommentAnalysis?sentence=文本'
        }
    }), mimetype='application/json')


@app.route('/alldata')
def alldata():
    roomid = request.args.get('roomid')
    msg_data = get_room_bullets(roomid)
    
    data_list = {}
    data_list["d1"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    t_list = []
    # 截取最新 12 条弹幕返回给前端
    show_data = msg_data[-12:] if len(msg_data) > 12 else msg_data
    for i in range(len(show_data) - 1, -1, -1):
        t_list.append(show_data[i])
        
    data_list['d2'] = t_list
    return Response(json.dumps(data_list), mimetype='application/json')


@app.route('/TimeRelatedAnalysis')
def TimeRelatedAnalysis():
    roomid = request.args.get('roomid')
    msg_data = get_room_bullets(roomid)
    
    time_list = []
    ymdhm = time.strftime("%Y-%m-%d %H", time.localtime())
    h = time.strftime("%H", time.localtime())
    
    for i in msg_data:
        if ymdhm in i:
            # 提取分钟
            time_list.append(i.split("*")[0].split(":")[1])
            
    data_time = list(set(time_list))
    data_time.sort()
    if len(data_time) > 7:
        data_time = data_time[-7:]

    name = [h + ":" + i for i in data_time]
    value = [time_list.count(i) for i in data_time]

    data_list = {
        "d1": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "name": name,
        "value": value
    }
    return Response(json.dumps(data_list), mimetype='application/json')


@app.route('/EmotionAnalysis')
def EmotionAnalysis():
    roomid = request.args.get('roomid')
    msg_data = get_room_bullets(roomid)
    
    count1, count2 = 0, 0
    for i in msg_data:
        try:
            text = i.split("*")[2]
            s = ModelApplication.ModelAnalysisCombinedBayes(text)
            if s > 0:
                count1 += 1
            else:
                count2 += 1
        except:
            continue
            
    data_list = {
        "d1": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "d2": [count1, count2]
    }
    return Response(json.dumps(data_list), mimetype='application/json')


@app.route('/getLiveStream')
def getLiveStream():
    """硬核方案：直接获取纯净的 FLV 视频流地址"""
    roomid = request.args.get('roomid')
    if not roomid:
        return Response(json.dumps({'code': '400', 'msg': 'Missing roomid'}), mimetype='application/json')
        
    try:
        # 1. 转换获取真实房间号
        init_res = requests.get(
            url=f"https://api.live.bilibili.com/room/v1/Room/room_init?id={roomid}",
            headers=conf.headers,
            timeout=5
        ).json()
        
        real_roomid = roomid
        if init_res.get('code') == 0:
            real_roomid = init_res.get('data', {}).get('room_id', roomid)
        # 2. 调用底层 API 抽取视频流地址 (quality=4 标清/高清, platform=web 会返回 flv 格式)
        play_url_res = requests.get(
            url=f"https://api.live.bilibili.com/room/v1/Room/playUrl?cid={real_roomid}&quality=4&platform=web",
            headers=conf.headers,
            timeout=5
        ).json()
        
        if play_url_res.get('code') == 0:
            durl = play_url_res.get('data', {}).get('durl', [])
            if durl and len(durl) > 0:
                # 拿到真正的底层的 .flv 视频流直链
                stream_url = durl[0].get('url')
                return Response(json.dumps({'code': '200', 'msg': 'SUCCESS', 'stream_url': stream_url}), mimetype='application/json')
            else:
                return Response(json.dumps({'code': '404', 'msg': '未找到直播流(可能未开播)'}), mimetype='application/json')
        else:
            return Response(json.dumps({'code': play_url_res.get('code'), 'msg': play_url_res.get('message')}), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'code': '500', 'msg': str(e)}), mimetype='application/json')

@app.route('/getBulletScreen')
def getBulletScreen():
    roomid = request.args.get('roomid')
    if not roomid:
        return Response(json.dumps({'code': '400', 'msg': 'Missing roomid'}), mimetype='application/json')

    bulletScreens = []
    try:
        # 1. 尝试获取真实房间号 (解决 B 站短号问题)
        init_res = requests.get(
            url=f"https://api.live.bilibili.com/room/v1/Room/room_init?id={roomid}",
            headers=conf.headers,
            timeout=5
        ).json()
        
        real_roomid = roomid
        if init_res.get('code') == 0:
            real_roomid = init_res.get('data', {}).get('room_id', roomid)
            if str(real_roomid) != str(roomid):
                print(f"短号 {roomid} 已转换为真实房间号: {real_roomid}")

        # 2. 爬取历史弹幕
        res = requests.get(
            url="https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory",
            headers=conf.headers,
            params={"roomid": real_roomid},
            timeout=5
        )
        res_json = res.json()
        
        # 3. 打印 B站官方返回的状态，方便排错
        code = res_json.get('code')
        msg = res_json.get('message')
        if code != 0:
            print(f"B站拒绝请求 -> code: {code}, message: {msg} (可能需要Cookie或IP被限)")
            
        bulletScreens = res_json.get('data', {}).get('room', [])
        if not bulletScreens:
            print(f"房间 [{real_roomid}] 当前无弹幕，或者未开播！")

    except Exception as e:
        print(f"接口请求完全失败: {e}")

    # 数据存入该房间号专用的列表中
    room_bullets = get_room_bullets(roomid)
    bsSet = set()
    
    for i in bulletScreens:
        nickname = i.get('nickname', '用户')
        text = i.get('text', '')
        timeline = i.get('timeline', time.strftime("%Y-%m-%d %H:%M:%S"))
        msg = f"{timeline}*{nickname}*{text}*{text}"
        bsSet.add(msg)

    # 去重并更新全局字典
    new_count = 0
    for msg in bsSet:
        if msg not in room_bullets:
            try:
                print(f"获取新弹幕: {msg.split('*')[2]}") # 打印爬到的新弹幕文本
            except UnicodeEncodeError:
                print(f"获取新弹幕: [包含特殊字符]")
            room_bullets.append(msg)
            new_count += 1
            
    # 防止列表无限增长撑爆内存，最多保留最近的 2000 条
    if len(room_bullets) > 2000:
        bullets_dict[roomid] = room_bullets[-2000:]

    return Response(json.dumps({'code': '200', 'msg': 'SUCCESS', 'new_count': new_count}), mimetype='application/json')


@app.route('/CommentAnalysis', methods=['GET', 'POST'])
def CommentAnalysis():
    # 兼容处理 Vue 前端发送的 form-data 参数
    list1 = request.form.get('sentence') or request.args.get('sentence')
    if not list1:
        if request.is_json:
            list1 = request.json.get('sentence')
            
    if not list1:
        return Response(json.dumps({"error": "No sentence provided"}), mimetype='application/json')

    sentence = re.sub(r'\W*', '', list1)
    if not sentence:
        sentence = list1 # 如果全是标点被去空了，就保留原样

    alist = {}
    try:
        data = ModelApplication.ModelAnalysisCombinedBayesByVectorDis(sentence)
        data1 = gv.unicode_vec(gv.generate_vector(sentence))
        
        # 挂载 4级网络欺凌 评估数据
        bully_result = calculate_bully_level(list1, data)
        
        alist['score'] = data
        alist['hot'] = data1
        alist['bully_eval'] = bully_result
    except Exception as e:
        print(f"分析出错: {e}")
        # 如果模型发生报错，进行容错兜底处理，确保前端不崩溃
        alist['score'] = 0.5
        alist['hot'] = ''
        alist['bully_eval'] = calculate_bully_level(list1, 0.5)

    return Response(json.dumps(alist), mimetype='application/json')





@app.route('/compare', methods=['POST'])
# @limiter.limit('1/5seconds')
def Compare():
    try:
        rawdata = request.get_data()
        jsondata = json.loads(rawdata)
        text = jsondata['sentence']
        examples, sentiments = CompareAnalysis.compareAnalysis(text)
        res = {'examples': examples, 'sentiments': sentiments}
    except Exception as e:
        res = {'examples': [], 'sentiments': []}
    return Response(json.dumps(res), mimetype='application/json')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        if not user_message:
            return Response(json.dumps({"reply": "消息不能为空"}), mimetype='application/json')
        
        reply = llm_service.chat(user_message)
        
        return Response(json.dumps({"reply": reply}), mimetype='application/json')
    except Exception as e:
        print(f"Chat Error: {e}")
        return Response(json.dumps({"reply": "AI 助手暂时走神了，请稍后再试"}), mimetype='application/json')

# end
if __name__ == "__main__":
    # threaded=True 防止单线程卡死
    app.run(host='0.0.0.0', port=conf.port, threaded=True, debug=False)
