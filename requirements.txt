import streamlit as st
from googleapiclient.discovery import build
from collections import Counter
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# NLTK 다운로드 (처음 실행 시 자동 다운로드)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

st.title("📺 YouTube Live Chat AI 분석기")

# ---------------------------------------------
# YouTube API 설정
# ---------------------------------------------
api_key = st.text_input("🔑 YouTube API Key 입력", type="password")
live_chat_id = st.text_input("💬 Live Chat ID 입력")

if st.button("분석 시작"):

    if not api_key or not live_chat_id:
        st.error("API Key와 Live Chat ID를 모두 입력해주세요.")
        st.stop()

    youtube = build("youtube", "v3", developerKey=api_key)

    messages = []
    next_page_token = None

    # ---------------------------------------------
    # 라이브 채팅 가져오기
    # ---------------------------------------------
    with st.spinner("라이브 채팅 불러오는 중..."):
        for _ in range(3):  # 여러 페이지 읽기 (원하면 늘릴 수 있음)
            chat_response = youtube.liveChatMessages().list(
                liveChatId=live_chat_id,
                part="snippet,authorDetails",
                pageToken=next_page_token
            ).execute()

            for item in chat_response["items"]:
                messages.append(item["snippet"]["displayMessage"])

            next_page_token = chat_response.get("nextPageToken")
            if not next_page_token:
                break

    if not messages:
        st.warning("채팅 메시지를 찾지 못했습니다.")
        st.stop()

    st.success(f"총 {len(messages)}개의 채팅 메시지를 가져왔습니다.")
    st.write(messages[:10])  # 일부 미리보기

    # ---------------------------------------------
    # 텍스트 정제 + 토큰화
    # ---------------------------------------------
    stop_words = set(stopwords.words("english") | stopwords.words("korean"))
    cleaned_words = []

    for msg in messages:
        msg = msg.lower()
        msg = re.sub(r"[^a-zA-Z가-힣0-9\s]", "", msg)
        words = word_tokenize(msg)
        words = [w for w in words if w not in stop_words and len(w) > 1]
        cleaned_words.extend(words)

    # ---------------------------------------------
    # 1) 어떤 단어가 많이 나왔는가?
    # ---------------------------------------------
    word_freq = Counter(cleaned_words)
    df_words = pd.DataFrame(word_freq.most_common(20), columns=["단어", "횟수"])
    st.subheader("📌 가장 많이 나온 단어 TOP 20")
    st.bar_chart(df_words.set_index("단어"))

    # ---------------------------------------------
    # 2) 어떤 주제의 대화인가? (간단한 keyword 기반 Topic)
    # ---------------------------------------------
    topics = {
        "AI / 기술": ["ai", "robot", "machine", "tech", "chatgpt", "api"],
        "게임": ["game", "fps", "lol", "valorant", "minecraft"],
        "정치": ["president", "election", "government"],
        "스포츠": ["sports", "soccer", "basketball", "football"],
        "음악": ["music", "song", "kpop", "idol"],
    }

    topic_scores = {k: 0 for k in topics}

    for w in cleaned_words:
        for topic, keywords in topics.items():
            if w in keywords:
                topic_scores[topic] += 1

    topic_df = pd.DataFrame(topic_scores.items(), columns=["주제", "관련 단어 수"])

    st.subheader("📌 채팅 주요 토픽 추정")
    st.bar_chart(topic_df.set_index("주제"))

    # ---------------------------------------------
    # 3) 어떤 의견이 제일 많은가? (감성 분석)
    # ---------------------------------------------
    sia = SentimentIntensityAnalyzer()

    sentiments = {"긍정": 0, "중립": 0, "부정": 0}

    for msg in messages:
        score = sia.polarity_scores(msg)
        if score["compound"] > 0.2:
            sentiments["긍정"] += 1
        elif score["compound"] < -0.2:
            sentiments["부정"] += 1
        else:
            sentiments["중립"] += 1

    sentiment_df = pd.DataFrame(sentiments.items(), columns=["감정", "개수"])

    st.subheader("📌 채팅 의견 감성 분석 결과")
    st.bar_chart(sentiment_df.set_index("감정"))
