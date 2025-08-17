from moviepy import (AudioFileClip, ImageClip, TextClip,
                            CompositeVideoClip, concatenate_audioclips,
                            concatenate_videoclips)
import os


os.environ["IMAGEMAGICK_BINARY"] = r"/usr/bin/convert"

def create_video_from_script(scenes, audio_paths):
    """장면 데이터와 오디오 경로를 기반으로 동영상을 생성합니다."""
    video_clips = []
    
    print("🎬 동영상 클립 생성을 시작합니다...")

    for scene in scenes:
        scene_number = scene['scene_number']
        narration_text = scene['narration'] # <--- 수정: 루프 안에서 나레이션 텍스트 정의
        audio_path = audio_paths.get(scene_number)
        
        if not audio_path or not os.path.exists(audio_path):
            print(f"⚠️ 경고: 장면 {scene_number}의 오디오 파일이 없어 건너뜁니다.")
            continue
        
        audio_clip = AudioFileClip(audio_path)
        clip_duration = audio_clip.duration
        
        image_path = scene.get('image_path')
        if not image_path or not os.path.exists(image_path):
            print(f"⚠️ 경고: 장면 {scene_number}의 이미지가 없어 건너뜁니다.")
            continue

        image_clip = ImageClip(image_path).with_duration(clip_duration)
        
        text_clip = TextClip(
            text=narration_text,
            font_size=70,
            color='white',
            font='/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf', 
            stroke_color='black',
            stroke_width=2,
            size=(980, None),
            method='caption'
        ).with_position(('center', 0.8), relative=True).with_duration(clip_duration)

        final_scene_clip = CompositeVideoClip([image_clip, text_clip])
        final_scene_clip = final_scene_clip.with_audio(audio_clip) # <--- 수정: 최신 문법 적용

        video_clips.append(final_scene_clip)
        print(f"✅ 장면 {scene_number} 클립 생성 완료 (이미지: {os.path.basename(image_path)})")
        # --- 여기까지 for 루프 안쪽 ---

    if not video_clips:
        print("❌ 생성된 클립이 없어 동영상을 만들 수 없습니다.")
        return

    final_video = concatenate_videoclips(video_clips) # <--- 수정: method="compose" 불필요
    final_video.resized(height=1920).write_videofile(
        "youtube_shorts_final.mp4", codec='libx265', audio_codec='aac', fps=24
    )
    print("🎉 최종 동영상 파일 'youtube_shorts_final.mp4'이(가) 성공적으로 생성되었습니다!")
