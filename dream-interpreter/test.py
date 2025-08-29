
from openai import OpenAI  # 導入 OpenAI SDK
client = OpenAI(api_key="sk-b1e7ea9f25184324aaa973412b081f6f", base_url="https://api.deepseek.com")
def interpret_dream(dream_content):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位專業的解夢專家，請解析夢境情緒並輸出格式如下：\n"
                                              "1. 焦慮 X%\n"
                                              "2. 恐懼 Y%\n"
                                              "3. 驚奇 Z%\n"
                                              "4. 希望 A%\n"
                                              "5. 困惑 B%"},
                {"role": "user", "content": dream_content}
            ],
            temperature=0.7,
            stream=False
        )
        interpretation = response.choices[0].message.content

        # 解析數字
        emotions = {
            "焦慮": 0, "恐懼": 0, "驚奇": 0, "希望": 0, "困惑": 0
        }
        for line in interpretation.split("\n"):
            match = re.match(r"(.+?)\s(\d+)%", line)
            if match:
                emotion, value = match.groups()
                if emotion in emotions:
                    emotions[emotion] = float(value)

        return interpretation, emotions

    except Exception as e:
        logging.error(f"夢境解析API調用失敗: {str(e)}", exc_info=True)
        return f"API 調用失敗: {str(e)}", None

interpretation, emotions = interpret_dream("我在海邊看到了一隻大海龜，它告訴我要好好保護海洋。")
print(interpretation, emotions) 
