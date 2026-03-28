import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 데이터베이스
song_db = {
    "밤편지": {
        "artist": "아이유",
        "melody": ["남", "△", "임", "△", "남", "△", "임", "고", "태", "황", "△", "△"],
        "lyrics": ["이", "-", "밤", "-", "그", "-", "날", "의", "반", "-", "-", "-"]
    },
    "어떻게이별까지사랑하겠어": {
        "artist": "AKMU",
        "melody": ["태", "태", "태", "태", "태", "황", "△", "△", "황", "태", "고", "임"],
        "lyrics": ["일", "부", "러", "몇", "발", "자", "국", "물", "어", "떻", "게", "이"]
    }
}

def make_jungganbo(song_name):
    # 사용자가 제목만 쳐도 인식되게 함 (공백 제거)
    target = song_name.replace(" ", "")
    if target not in song_db:
        return "노래를 찾을 수 없소! 현재 '밤편지', '어떻게이별까지사랑하겠어'만 가능하오."
    
    data = song_db[target]
    m, l = data["melody"], data["lyrics"]
    
    res = f"🤖 정간봇: {data['artist']} - {target}\n\n"
    res += "┌──┬──┬──┬──┐\n"
    for i in range(0, len(m), 4):
        res += "│" + "│".join(f"{x:^2}" for x in m[i:i+4]) + "│\n"
        res += "│" + "│".join(f"({x:^1})" for x in l[i:i+4]) + "│\n"
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
    except Exception as e:
        answer = "오류가 발생했소! 서버 로그를 확인해보시오."

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": answer}}]
        }
    })

if __name__ == '__main__':
    # Render 환경변수 PORT를 우선 사용
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
