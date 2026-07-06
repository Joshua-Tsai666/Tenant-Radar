import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_rent_content(text: str) -> dict:
    """使用 OpenAI 將純文字轉為結構化 JSON 數據"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 2026年高性價比首選模型
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是一個台灣租屋市場的資料分析師。請分析使用者的求租貼文，"
                        "並精確提取出欄位。請一律回傳標準 JSON 格式，不要包含任何 markdown 標記（如 ```json）。"
                        "欄位規範如下：\n"
                        "- location: 縣市與行政區（例如：台北市大安區）\n"
                        "- budget_max: 整數，預算上限（例如：15000，若沒寫填 0）\n"
                        "- room_type: 房型（例如：獨立套房、整層住家、雅房）\n"
                        "- identity: 租客身份（例如：工程師、女大生、情侶）"
                    )
                },
                {"role": "user", "content": text}
            ],
            temperature=0.0
        )
        # 解析 AI 回傳的 JSON 字串
        result = json.loads(response.choices[0].message.content.strip())
        return result
    except Exception as e:
        print(f"AI 解析失敗: {e}")
        return {"location": "未知", "budget_max": 0, "room_type": "未知", "identity": "未知"}
