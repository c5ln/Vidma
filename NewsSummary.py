import os
import requests
import google.generativeai as genai

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
    
    Here is the original text:
    ---
    {original_text}
    ---
    Now, generate the script based on the text above.
    """

def generate_script_from_text(original_text):
    # (이전에 만든 Gemini 호출 함수와 동일)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = create_script_prompt(original_text)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API 호출 중 오류가 발생했습니다: {e}")
        return None


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