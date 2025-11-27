import streamlit as st
import re

st.title("📺 YouTube 썸네일 다운로드 사이트")

st.write("유튜브 영상 URL을 입력하면 썸네일을 자동으로 가져옵니다.")

# ---------------------------------------------
# 유튜브 URL에서 Video ID 추출
# ---------------------------------------------
def extract_video_id(url):
    pattern = r"(?:v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# ---------------------------------------------
# 입력창
# ---------------------------------------------
url = st.text_input("🎥 YouTube URL 입력")

if url:
    video_id = extract_video_id(url)

    if video_id:
        st.success(f"Video ID 찾음: {video_id}")

        # 유튜브 썸네일 URL
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

        st.image(thumbnail_url, caption="YouTube 썸네일 미리보기")

        st.write("📥 아래 링크를 클릭해 썸네일을 다운로드하세요:")
        st.markdown(f"[썸네일 다운로드]({thumbnail_url})")
    else:
        st.error("유효한 YouTube URL이 아닙니다.")
