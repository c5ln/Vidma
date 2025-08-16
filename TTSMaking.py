from gtts import gTTS

script_text = "This is a sample script for our automated short video."

# gTTS 객체 생성
tts = gTTS(text=script_text, lang='en')

# 파일로 저장
tts.save("narration.mp3")

print("narration.mp3 파일이 생성되었습니다!")