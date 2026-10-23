import asyncio
import os
from google import genai
import edge_tts

# 同時檢查 "ai" 或 "GEMINI_API_KEY" 這兩個名稱，確保一定抓得到
GEMINI_API_KEY = os.environ.get("ai") or os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("找不到 API Key！請檢查 GitHub Secrets 是否有名為 'ai' 的設定。")

client = genai.Client(api_key=GEMINI_API_KEY)

VOICE = "zh-TW-HsiaoChenNeural"
OUTPUT_FILE = "dj_speech.mp3"

def generate_dj_script():
    prompt = """
    你是一位風格專業的網路電台 DJ。
    請寫一段大約 30 到 200 字的廣播串場詞，向收聽的聽眾打招呼，並預告接下來要播放的音樂。
    語氣要自然、像真人在說話，不要加入任何括號說明或情緒提示。直接給出要唸出來的文字即可。請使用繁體中文對話 這是FRX Radio
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()

async def text_to_speech(text, output_path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)

async def main():
    print("🤖 雲端大腦啟動：正在讓 Gemini 撰寫 DJ 台詞...")
    script = generate_dj_script()
    print(f"【台詞】: {script}")

    print("🎙️ 正在生成語音檔...")
    await text_to_speech(script, OUTPUT_FILE)
    print("✨ 語音檔生成完畢！")

if __name__ == "__main__":
    asyncio.run(main())
