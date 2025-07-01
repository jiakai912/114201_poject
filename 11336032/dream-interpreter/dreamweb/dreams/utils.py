from pydub import AudioSegment
import tempfile
import os

def convert_to_wav(audio_file):
    try:
        # 使用 pydub 轉換音檔格式
        audio = AudioSegment.from_file(audio_file)
        temp_wav_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio.export(temp_wav_file.name, format="wav")
        return temp_wav_file.name  # 返回臨時 WAV 文件的路徑
    except Exception as e:
        raise ValueError("音檔轉換錯誤") from e
