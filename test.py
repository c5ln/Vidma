# font_test.py
from moviepy import TextClip

print("--- Font Test Script Running ---")

try:
    # Test 1: Using the font name
    print("Attempting to create clip with font name 'NanumGothic-Bold'...")
    clip1 = TextClip(
        "테스트 1",
        font="NanumGothic-Bold",
        fontsize=70,
        color='white'
    )
    print("✅ Test 1 Succeeded!")

    # Test 2: Using the full file path
    print("\nAttempting to create clip with full font path...")
    clip2 = TextClip(
        "테스트 2",
        font="/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
        fontsize=70,
        color='white'
    )
    print("✅ Test 2 Succeeded!")
    
    print("\n--- Both tests passed. Your environment seems OK. ---")
    print("The error is likely in your main VideoMaker.py script's TextClip call.")

except Exception as e:
    print("\n❌ TEST FAILED.")
    print("This confirms the issue is with your system's MoviePy or ImageMagick configuration.")
    print("Error details:", e)