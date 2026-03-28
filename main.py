import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# [소박 지원 DB] 리스트 안에 또 리스트가 있으면 소박으로 처리합니다.
song_db = {
    "밤편지": {
        "artist": "아이유",
        "melody": [
            "남", "△", "임", "△", "남", "△", "임", "고", 
            "태", "황", "△", "△", "태", "태", "황", "△", 
            "남", "△", "임", "고", "태", "황", "△", "△",
            "태", "황", "태", "고", "임", "△", "△", "△", 
            ["고", "태"], "황", "△", "△", "태", "태", "황", "△"  # [고태] 부분이 소박!
        ],
        "lyrics": [
            "이", "-", "밤", "-", "그", "-", "날", "의", 
            "반", "-", "-", "-", "딧", "불", "을", "-", 
            "당", "-", "신", "의", "창", "-", "-", "-",
            "가", "까", "이", "-", "보", "-", "-", "-", 
            "사랑", "한", "다", "는", "말", "-", "이", "에"
        ]
    }
}

def format_cell(data, is_lyric=False):
    """한 칸에 데이터가 여러 개(리스트)면 소박 형식으로 변환"""
    if isinstance(data, list):
        content = "".join(data)
        return f"[{content}]" if not is_lyric else f"({content})"
    return f"{data}" if not is_lyric else f"({data})"

def make_jungganbo(song_name):
    target = song_name.replace(" ", "")
    if target not in song_db:
        return "없는 곡입니다."
    
    data = song_db[target]
    m, l = data["melody"], data["lyrics"]
    
    res = f"🤖 정간봇: {data['artist']} - {target}\n\n"
    res += "┌──┬──┬──┬──┐\n"
    
    for i in range(0, len(m), 4):
        # 율명 라인 처리
        m_line = [format_cell(x) for x in m[i:i+4]]
        res += "│" + "│".join(f"{x:^2}" for x in m_line) + "│\n"
        
        # 가사 라인 처리
        l_line = [format_cell(x, True) for x in l[i:i+4]]
        res += "│" + "│".join(f"{x:^2}" for x in l_line) + "│\n"
        
        if i + 4 < len(m):
            res += "├──┼──┼──┼──┤\n"
            
    res += "└──┴──┴──┴──┘"
    return res

@app.route('/api/junggan', methods=['POST'])
def chat():
    try:
        body = request.get_json()
        user_text = body['userRequest']['utterance']
        answer = make_jungganbo(user_text)
    except:
        answer = "서버에 오류가 생겼습니다!"

    return jsonify({
        "version": "2.0",
        "template": {"outputs": [{"simpleText": {"text": answer}}]}
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
