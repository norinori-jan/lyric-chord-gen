import os
import platform
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

def get_icloud_path():
    """OSに応じてiCloud Driveのルートパスを返す（Windows/Mac両対応）"""
    home = os.path.expanduser("~")
    system = platform.system()
    if system == "Darwin": # Mac
        return os.path.join(home, "Library/Mobile Documents/com~apple~CloudDocs")
    elif system == "Windows": # Windows
        return os.path.join(home, "iCloudDrive")
    return os.path.join(os.getcwd(), "output") # その他

# --- 設定 ---
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SERVICE_REGION = os.getenv("AZURE_SERVICE_REGION")
APP_FOLDER_NAME = "MyLyricApp"
SAVE_PATH = os.path.join(get_icloud_path(), APP_FOLDER_NAME)

def generate_speech(text, filename):
    if not AZURE_SPEECH_KEY:
        print("❌ エラー: .envファイルにAPIキーが設定されていません。")
        return

    # 保存先フォルダを作成
    os.makedirs(SAVE_PATH, exist_ok=True)
    
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SERVICE_REGION)
    # 日本語の自然な女性の声「Nanami」
    speech_config.speech_synthesis_voice_name = "ja-JP-NanamiNeural"
    
    file_full_path = os.path.join(SAVE_PATH, f"{filename}.wav")
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_full_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    print(f"🎤 音声を生成中...: {text}")
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"✅ 成功！保存完了: {file_full_path}")
    else:
        print(f"❌ エラー発生: {result.reason}")

if __name__ == "__main__":
    # テスト用の歌詞
    test_lyrics = "自動保存の仕組みを、今ここから始めよう。"
    generate_speech(test_lyrics, "startup_voice")