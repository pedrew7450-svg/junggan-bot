import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# [소박 지원 DB] 리스트 안에 또 리스트가 있으면 소박으로 처리합니다.
song_db = {
    "밤편지": {
        "artist": "아이유",
        "melody": [
            "남", "△", "임", "△", "남", "△", "임", "고",  # 이 밤 그날의
            "태", "황", "△", "△", "태", "태", "황", "△",  # 반딧불을 당신의
            "남", "△", "임", "고", "태", "황", "△", "△",  # 창 가까이 보낼게요
            "태", "황", "태", "고", "임", "△", "△", "△",  # 음- 사랑한다는
            ["남", "남"], "△", "임", "고", "태", "황", "△", "△",  # 말이에요 나 우리
            "태", "태", "황", "△", ["고", "태"], "태", "황", "△",  # 의 첫 입맞춤을 떠
            "남", "△", "임", "고", "태", "황", "△", "△",  # 올려 그럼 언제든
            "태", "황", "태", "고", "임", "△", "△", "△",  # 눈을 감고 음- 
            "남", "△", "임", "고", "태", "황", "△", "△",  # 가장 먼 곳으로 
            "태", "태", "황", "△", "황", "△", "△", "△"   # 가요-
        ],
        "lyrics": [
            "이", "-", "밤", "-", "그", "-", "날", "의",
            "반", "-", "-", "-", "딧", "불", "을", "-",
            "당", "-", "신", "의", "창", "-", "-", "-",
            "가", "까", "이", "-", "보", "-", "-", "-",
            "낼", "게", "요", "-", "음", "-", "-", "-",
            "사", "랑", "한", "다", "는", "말", "이", "에",
            "요", "-", "나", "-", "우", "리", "의", "-",
            "첫", "입", "맞", "춤", "을", "-", "-", "-",
            "떠", "올", "려", "-", "그", "럼", "언", "제",
            "든", "-", "-", "-", "눈", "을", "감", "고"
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
        # [추가] 메뉴/목록 기능
    if target in ["메뉴", "목록", "노래목록", "help", "도움말"]:
        song_list = "\n".join([f"🎵 {k} ({v['artist']})" for k, v in song_db.items()])
        return f" 정간봇 수록곡 리스트 \n\n{song_list}\n\n원하는 곡 제목을 정확히 입력해주세요"
    
    data = song_db[target]
    m, l = data["melody"], data["lyrics"]
    
    res = f"🤖 정간봇: {data['artist']} - {target}\n\n"
    res += "┌──┬──┬──┬──┐\n"
    
    for i in range(0, len(m), 4):
        # 율명 라인 처리
        m_line = [format_cell(x) for x in m[i:i+4]]
        res += "│" + "│".join(f"{x:^1}" for x in m_line) + "│\n"
        
        # 가사 라인 처리
        l_line = [format_cell(x, True) for x in l[i:i+4]]
        res += "│" + "│".join(f"{x:^1}" for x in l_line) + "│\n"
        
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
