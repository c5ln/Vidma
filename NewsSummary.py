import os
import requests
import google.generativeai as genai
import TtsMaker as ttsMaker
import VideoMaker as videoMaker
import ImageFinder as imageFinder

from dotenv import load_dotenv

load_dotenv()
# --- API 키 설정 ---
# 1. Google Gemini API 키
# os.environ['GOOGLE_API_KEY'] = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# 2. Alpha Vantage API 키
# os.environ['ALPHA_VANTAGE_API_KEY'] = "YOUR_ALPHA_VANTAGE_API_KEY"


# --- 함수 정의 (이전 단계에서 만든 함수들) ---

def get_news_from_alpha_vantage(topic="technology"):
    # (위의 2단계 코드와 동일)
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        print("ALPHA_VANTAGE_API_KEY 환경 변수를 설정해주세요.")
        return None
    url = 'https://www.alphavantage.co/query'
    params = {'function': 'NEWS_SENTIMENT', 'topics': topic, 'apikey': api_key, 'limit': 1}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'feed' in data and len(data['feed']) > 0:
            return data['feed'][0]['summary']
        else:
            print(f"뉴스 데이터를 가져오지 못했습니다: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류가 발생했습니다: {e}")
        return None

def create_script_prompt(original_text):
    # (이전에 만든 프롬프트 템플릿과 동일)
    return f"""
    You are a professional scriptwriter for short-form videos.
    Your task is to transform the following original text into a compelling script for a 1-minute YouTube Shorts video.
    Please follow these rules:
    1. The tone should be engaging and easy for the general public to understand.
    2. The script must be divided into scenes.
    3. For each scene, provide a "SCENE", "VISUAL", and "NARRATION".
    
    Template : 
    SCENE: #1
    VISUAL: Quick, dynamic cuts...
    NARRATION: Think Roku is just...
    
    Here is the original text:
    ---
    {original_text}
    ---
    Now, generate the script based on the text above. VISUAL은 영어로 적고, NARRATION은 한글로 적어줘.
    """

def generate_script_from_text(original_text):
    # (이전에 만든 Gemini 호출 함수와 동일)
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = create_script_prompt(original_text)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API 호출 중 오류가 발생했습니다: {e}")
        return None


def get_keywords_from_text(text):
    """Gemini를 이용해 텍스트에서 이미지 검색용 키워드를 추출합니다."""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Analyze the following news text and extract the 3 most relevant keywords for searching stock images.
    Return the keywords as a comma-separated list. For example: 'AI, semiconductor, technology'

    TEXT:
    ---
    {text}
    ---
    
    KEYWORDS:
    """
    
    try:
        response = model.generate_content(prompt)
        # 쉼표로 분리하고 양쪽 공백 제거
        keywords = [keyword.strip() for keyword in response.text.split(',')]
        return keywords
    except Exception as e:
        print(f"키워드 추출 중 오류 발생: {e}")
        return []

def parse_script(script_text): # 입력 변수 이름을 'script_text'로 변경
    """대본 텍스트(문자열)를 직접 파싱합니다."""
    if not script_text: # None 값이 들어올 경우를 대비
        return []
        
    scenes = []
    # 텍스트를 'SCENE:' 기준으로 분리하여 각 장면 처리
    raw_scenes = script_text.strip().split('SCENE:')[1:]
    
    for i, scene_block in enumerate(raw_scenes, 1):
        current_scene = {'scene_number': f'#{i}', 'visual': '', 'narration': ''}
        lines = scene_block.strip().split('\n')
        for line in lines:
            if 'VISUAL:' in line:
                current_scene['visual'] = line.split('VISUAL:', 1)[1].strip()
            elif 'NARRATION:' in line:
                current_scene['narration'] = line.split('NARRATION:', 1)[1].strip()
        scenes.append(current_scene)
    return scenes

def get_keywords_from_visual(visual_desc):
    """Gemini를 이용해 VISUAL 설명에서 이미지 검색용 키워드를 추출합니다."""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are an expert at finding stock photos. Analyze the following scene description and extract 2-3 perfect, searchable keywords for Pexels.
    Return only the keywords as a comma-separated list. For example: 'skeptical person, streaming stick'

    SCENE DESCRIPTION:
    ---
    {visual_desc}
    ---
    
    KEYWORDS:
    """
    
    try:
        response = model.generate_content(prompt)
        keywords = [keyword.strip() for keyword in response.text.split(',')]
        print(f"🔍 추출된 키워드: {keywords}")
        return keywords
    except Exception as e:
        print(f"키워드 추출 중 오류 발생: {e}")
        return []
# 대본 파일 경로

# --- 메인 실행 로직 ---
if __name__ == "__main__":
    print("📈 Alpha Vantage에서 최신 기술 뉴스를 가져옵니다...")
    # 1. Alpha Vantage에서 뉴스 텍스트를 가져옴
    news_summary = get_news_from_alpha_vantage(topic="technology")
   
    if news_summary:
        print("📰 뉴스 요약본을 성공적으로 가져왔습니다.")
        print("--------------------")
        print(news_summary)
        print("--------------------")
        print("🤖 Gemini를 이용해 대본을 생성합니다...")
        
        # 2. 가져온 텍스트를 Gemini에 전달하여 대본 생성
        generated_script = generate_script_from_text(news_summary)
        
        if generated_script:
            print("\n--- ✅ 최종 생성된 쇼츠 대본 ---")
            print(generated_script)

        # 3. 대본 파싱
        parsed_scenes = parse_script(generated_script)

        # 4. 나레이션 mp3 파일 생성
        narration_paths = ttsMaker.create_narration_files(parsed_scenes)
    
        # 5. 각 장면에 맞는 이미지 검색 및 다운로드
        print("\n🖼️ Pexels에서 각 장면에 맞는 이미지를 검색하고 다운로드합니다...")
        for scene in parsed_scenes:
             # Gemini를 통해 VISUAL 설명에서 핵심 키워드를 추출합니다.
            keywords = get_keywords_from_visual(scene['visual'])

            if keywords:
                image_files = imageFinder.search_pexels_and_download(keywords, count=1)
                if image_files:
                # 다운로드된 첫 번째 이미지 경로를 scene 딕셔너리에 추가
                    scene['image_path'] = image_files[0]

        # 6. 최종 동영상 생성
        videoMaker.create_video_from_script(parsed_scenes, narration_paths)