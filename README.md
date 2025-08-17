# Vidma
short vidio maker

서비스 설명 
1. 주어진 텍스트 기반으로 Gemini를 통해 동영상 대본을 만든다.
2. Moviepy를 이용해 영상으로 만든다.
3. 다 되면 slack으로 알람이 간다
4. 승인을 하면 자동으로 유튜브에 올라간다.

흐름
1. Alpha Vantage 에서 Technology topic을 가진 기사를 가져온다. 
2. 가져온 기사를 기반으로 Gemini를 이용해 대본을 만든다.
3. 만든 대본을 기반으로 gTTS를 이용해서 나레이션 파일을 만든다.
4. 대본을 기반으로 Pexles 에서 이미지를 가져온다.
5. 대본과 나레이션 파일 이미지를 MoviePy로 합친다.
=> 동영상 제작 완료