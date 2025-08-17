
import os 
import pexelsPy 
import requests
from dotenv import load_dotenv

load_dotenv()


PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

def search_pexels_and_download(keywords, output_dir="images", count=1):
    """Pexels에서 이미지를 검색하고 다운로드한 뒤, 로컬 파일 경로 리스트를 반환합니다."""
    if not PEXELS_API_KEY:
        print("PEXELS_API_KEY를 설정해주세요.")
        return []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        api = pexelsPy.API(PEXELS_API_KEY)
    except Exception as e:
        print(f"PEXELS API 인증 중 오류 발생: {e}")
        return []
        
    local_image_paths = []
    
    search_query = " ".join(keywords)
    
    # 'search' -> 'search_photos'로 변경
    search_results = api.search_photos(query=search_query, page=1, results_per_page=count)
    
    # 반환된 결과에서 'photos' 리스트를 직접 가져옴
    photos = search_results.get('photos', [])
    
    if not photos:
        print(f"'{search_query}'에 대한 이미지를 찾을 수 없습니다.")
        return []

    for photo in photos:
        # photo 객체가 딕셔너리 형태로 반환되므로 접근 방식 변경
        image_url = photo['src']['large']
        photographer = photo['photographer']
        photo_id = photo['id']
        
        try:
            response = requests.get(image_url)
            file_name = f"pexels_{photographer.replace(' ', '_')}_{photo_id}.jpg"
            file_path = os.path.join(output_dir, file_name)
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            local_image_paths.append(file_path)
            print(f"✅ 이미지 다운로드 완료: {file_path}")
        except Exception as e:
            print(f"❌ 이미지 다운로드 실패 (URL: {image_url}): {e}")

    return local_image_paths