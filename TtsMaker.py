from gtts import gTTS
import os

def create_narration_files(scenes, output_dir="narrations"):
    """
    파싱된 장면 리스트를 받아 각 장면의 나레이션을 mp3 파일로 저장합니다.
    """
    # 나레이션 파일을 저장할 폴더 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"'{output_dir}' 폴더를 생성했습니다.")

    audio_files = {}
    print("장면별 나레이션 파일 생성을 시작합니다...")
    
    for scene in scenes:
        narration_text = scene.get('narration')
        scene_number_simple = scene.get('scene_number').replace('#', '')
        # --- 디버깅용 print문 추가 ---
        print(f"\n--- [장면 {scene_number_simple} 처리 시작] ---")
        print(f"나레이션 텍스트: '{narration_text}'")
        # ---------------------------
        if not narration_text:
            print(f"장면 {scene_number_simple}에는 나레이션이 없어 건너뜁니다.")
            continue

        try:
            # gTTS 객체 생성 (lang='ko'로 한국어 설정)
            tts = gTTS(text=narration_text, lang='ko')
            
            # 파일 저장 경로 설정 (예: narrations/narration_1.mp3)
            file_path = os.path.join(output_dir, f"narration_{scene_number_simple}.mp3")
            
            # 파일로 저장
            tts.save(file_path)
            
            # MoviePy에서 사용할 수 있도록 파일 경로 저장
            audio_files[scene.get('scene_number')] = file_path
            print(f"✅ 장면 {scene_number_simple}의 나레이션 저장 완료: {file_path}")

        except Exception as e:
            print(f"❌ 장면 {scene_number_simple} 처리 중 오류 발생: {e}")
            
    return audio_files
