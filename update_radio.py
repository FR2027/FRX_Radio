import asyncio
import os
from google import genai
import edge_tts

# 從 GitHub Secrets 讀取 API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

VOICE = "zh-TW-HsiaoChenNeural"
OUTPUT_FILE = "dj_speech.mp3"

def generate_dj_script():
    prompt = """
    你是一位風格輕鬆、親切的網路電台 DJ。
    請寫一段大約 30 到 50 字的廣播串場詞，向深夜收聽的聽眾打招呼，並預告接下來要播放放鬆的音樂。
    語氣要自然、像真人在說話，不要加入任何括號說明或情緒提示。直接給出要唸出來的文字即可。
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
