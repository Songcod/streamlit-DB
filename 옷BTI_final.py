import streamlit as st
import pandas as pd
import numpy as np
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# # Authenticate with Google Sheets API
# scope = ['https://spreadsheets.google.com/feeds',
#          'https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name('db3clothbtitest-94a9d95273f4.json', scope)
# client = gspread.authorize(creds)


# # Open the spreadsheet and select the worksheet by name
# spreadsheet = client.open('DB_설문조사')
# worksheet = spreadsheet.worksheet('응답')


# Function to handle Google Sheets API interactions
def interact_with_gsheet(action, spreadsheet_name, worksheet_name, data=None):

    # Setup the Google Sheets API client
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('db3clothbtitest-94a9d95273f4.json', scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet
    spreadsheet = client.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet(worksheet_name)

    if action == 'fetch':
        # Fetch all records from the worksheet
        data = worksheet.col_values(8)
        return data
    elif action == 'append' and data is not None:
        # Append a new row to the worksheet
        worksheet.append_row(data)
        return None

def set_page_style():
    st.markdown("""
    <style>
    /* 앱 전체 스타일 조정 */
    .stApp {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    /* 버튼 기본 스타일 */
    .stButton>button {
        border: 2px solid rgba(128, 128, 128, 0.5);
        background-color: transparent; /* 버튼 기본 배경색 제거 */
        color: rgb(0, 0, 0); /* 버튼 기본 텍스트 색상 */
        padding: 10px 24px;
        border-radius: 20px;
        font-size: 16px;
        display: block;
        margin: 20px auto;
        width: fit-content;
    }
    /* 버튼 호버 스타일 */
    .stButton>button:hover {
        border: 2px solid rgba(0, 0, 0, 0.1);
        background-color: rgb(255, 215, 0); /* 호버 시 색상 채우기 */
        color: white;
    }
    /* 이미지 스타일 조정 */
    .stImage>img {

        margin-bottom: 20px; /* 이미지와 텍스트 사이 간격 */
    }
    /* 설문 질문 글꼴 크기 확대 */
    .markdown-text-container, .stMarkdown {
        text-align: center !important;
        font-size: 16px !important; /* 글꼴 크기 조정 */
    }
    </style>
    """, unsafe_allow_html=True)


# 페이지 설정 및 CSS 스타일 적용
st.set_page_config(page_title="옷BTI 테스트", layout="wide")
set_page_style()  # 페이지 스타일 설정을 여기에 호출하여 모든 페이지에 적용

questions = [
    ("1. ‘오늘부터 단 7일! 고객님만을 위한 특별 할인 쿠폰!’ 카톡이 울렸다. 이때 나의선택은?", 
     ["옷을 살 생각은 없었지만 세일을 한다고 하니 일단 구경한다.", 
      "딱히 옷을 사려고 생각하지 않았으니 무시한다."], 
      "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihb9nGSbmWOjWMgJSyLZtzVbXJx4bOsNFr-QwZg5u8ilskQ6OniEaiwXKMchgCYebFiT-nQLmT2_XWtFzbMYxnXRQ87vZqUJZw=w959-h912-rw-v1"),
    ("2. 앗! 쿠폰이 오늘 사라져요! 고객님이 보유하신 쿠폰이 오늘 만료될 예정입니다.", 
     ["엇!! 내가 호옥시나 필요한 옷이 있을 수도 있으니 12시가 되기 전까지 시간될 때마다 웹서핑을 계속한다.", 
      "이런 타임 어택으로 옷을 사면 실패하거나 충동 구매할 확률이 높으니 다음 기회에!"], 
      "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihag9UwpiUp7Zlrym9ZtaqjjUjKXcUR1BB3lfS4l0mqhXzNK-5uWfOw-i7WWmy_7KkcuaDayTF1Z6Ne2gpUCX2zwdIDLP6yJNA=w959-h912-rw-v1"),
    ("3. 새학기를 맞아 대청소를 결심하고 옷장 문을 열었더니", 
     ["오래 입지 않아 있는 줄도 몰랐던 옷들이 한 무더기로 발견된다.", 
      "매년 옷장 정리를 했기 때문에 어떤 옷들이 있는지 잘 알고 있다."], 
      'https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihaidVZ-dbeANunEU6F0118KCYoPLu26krEnPqL67Q57DOkaD9gnEy6I1__h1q_uDTaIm7t-JQLbhqBBCa97oKbvDH-GEo32vBs=w959-h912-rw-v1'),
    ("4. 둘 중 하나를 구매해야 한다면?", 
     ["친환경 소재와 공정을 사용해 만든 코트", 
      "최신 트렌드를 반영해 만든 올해의 SS 상품"], 
     "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihbA7BGQ6HpH6jTnj3JmAC5dvtb27T0wgPAqkzDBjVs1EzTFJsCbUX7WJk2993HpGNpFVN6ruhn6o2wAE5TbEszfB-lsu4FQyqI=w959-h912-rw-v1"),
    ("5. 오늘은 개강 첫 주! 아쉽게도 이번 학기는 공강이 없는데,,,", 
     ["적어도 일주일동안 겹치지 않고 입을 정도의 옷들은 있어야지!! 바로 쇼핑을 시작한다.", 
      "에이! 내 옷을 누가 알아본다고!! 적당히 돌려 입는다."], 
     "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihYLwestCH7UMtm3ti26PmPtXSndHKjhdS69n3FqbwshTH4cUhjfKOtxLhOye-uMcflAINka3jqdac_GgCADQ3h9LjE0zR_C7Ys=w959-h912-rw-v1"),
    ("6. 옷장정리를 해서 안 입는 옷을 박스에 담았다. 이때 나의 선택은?", 
     ["에이… 언젠간 입겠지. 버리긴 아까우니 입을 일이 있을 때까지 놔둔다.", 
      "난 안 입지만 괜찮은 옷들인데… 헌옷 기부처를 알아본다.",
      "이번 기회에 리폼을 한 번 해볼까? 유튜브에 긴 청바지 리폼 방법을 찾아본다."], 
     "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihZ-vkz43LyY_XCLUimR9ZxW76xX5h0LH7QRh6yxxufSJmjtnEgxr5jMXj94ckkRMcTPXT2EyxbXiZ2YoO9C8qR4RUd2XC9CGrI=w959-h912-rw-v1"),
     ("7. 우리집 앞에 옷 가게가 생긴다면 내가 더 애용할 곳은?", 
     ["상태가 좋은 구제 옷들을 이용해 다양한 코디를 선보이는 구제샵", 
      "값싼 소재의 옷을 이용해 가성비 좋게 옷을 구매할 수 있는 가게"], 
     "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihZlW4PhQM8jgB_eujk32hVk_U-CjxcDkapDI5v2cFZ-_bo8lSVPcOA_JaBIJq60ZySOaEjvw6A-wbHyMzqKzW2H6I-bPQbGSQQ=w959-h912-rw-v1")
]

# 앱의 초기 설정 부분에서 응답 DataFrame을 초기화합니다.
if 'responses_df' not in st.session_state:
    columns = [f"Question {i+1}" for i in range(len(questions))]
    st.session_state.responses_df = pd.DataFrame(columns=columns)

score_dict = {
    #1
    "옷을 살 생각은 없었지만 세일을 한다고 하니 일단 구경한다." : 5, 
    "딱히 옷을 사려고 생각하지 않았으니 무시한다." : 0,
    #2
    "엇!! 내가 호옥시나 필요한 옷이 있을 수도 있으니 12시가 되기 전까지 시간될 때마다 웹서핑을 계속한다." : 5, 
    "이런 타임 어택으로 옷을 사면 실패하거나 충동 구매할 확률이 높으니 다음 기회에!" : 0,
    #3
    "오래 입지 않아 있는 줄도 몰랐던 옷들이 한 무더기로 발견된다." : 5, 
    "매년 옷장 정리를 했기 때문에 어떤 옷들이 있는지 잘 알고 있다." : 0,
    #4
    "친환경 소재와 공정을 사용해 만든 코트" : 0, 
    "최신 트렌드를 반영해 만든 올해의 SS 상품" : 5,
    #5
    "적어도 일주일동안 겹치지 않고 입을 정도의 옷들은 있어야지!! 바로 쇼핑을 시작한다." : 5, 
    "에이! 내 옷을 누가 알아본다고!! 적당히 돌려 입는다." : 0,
    #6
    "에이… 언젠간 입겠지. 버리긴 아까우니 입을 일이 있을 때까지 놔둔다." : 0, 
    "난 안 입지만 괜찮은 옷들인데… 헌옷 기부처를 알아본다." : 5,
    "이번 기회에 리폼을 한 번 해볼까? 유튜브에 긴 청바지 리폼 방법을 찾아본다." : 5,
    #7
    "상태가 좋은 구제 옷들을 이용해 다양한 코디를 선보이는 구제샵" : 0, 
    "값싼 소재의 옷을 이용해 가성비 좋게 옷을 구매할 수 있는 가게" : 5
    }

# Find the maximum number of options in any question
max_options = max(len(options) for _, options, _ in questions)

# Initialize or update the response tracker
if 'response_tracker' not in st.session_state:
    st.session_state['response_tracker'] = pd.DataFrame(0, 
                                                        index=np.arange(len(questions)), 
                                                        columns=[f"Option {i+1}" for i in range(max_options)])
    st.session_state['page'] = 'cover'  # 현재 cover 페이지에 있다고 설정
    st.session_state['question_index'] = 0  # 첫 질문부터 시작
    st.session_state['selected_options'] = []  # 아직 옵션 선택 부분을 빈칸으로


def display_cover():
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihbOWOVf4pxlMZnOeA194VvO3brD0aI5o9IIJymSHmbw18GwaClXDdzbG_4nn6bo0nmaJMqQo3LxLZ0e8zk-VlDKj65Q0N1oNA=w959-h912-rw-v1" style="width: 384px; height:384px; max-height: 24rem;">
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if st.button("Start", key="start"):
        st.session_state['page'] = 'intro'
        st.rerun()


    st.markdown("## 찍찍이 현황")
    col1, col2, col3, col4 = st.columns(4)

    # 캐릭터 순서와 이미지 URL을 업데이트
    images = [
        "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihZVPtbjqbk6VO6nYUulBhzo9jMfw1Fe8CW8evIZKj2fYxSUzx-VGbZBkio5BHuEdOyfXHP-RMl0Le9Tv8KlogFXNTRBhs2O4w=w959-h912-rw-v1",  # 트렌드탐험대장
        "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpiha5FhG-uc3zo3Qd8z3X8uwWzQw2cOO32sL2fJyQV6DXxZQgXiaWhueKptxiTOReMa1GffVniu7hnEpYUnLxrT5mCs84vk1-wFI=w959-h912-rw-v1",  # 모던스타일리스트
        "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpiha3SyI5t6muk9d9gQHZNv7mOooVaTTHRyo9DP8NW-zyh5kT4h1xszghHYcZIiPEytTKPvEN0xnYhz0Pj9CrmT3jfVajQOtuxQ=w959-h912-rw-v1",  # 그린스타일리스트
        "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpiha4ebicanovZHhyCFdVZJL0LYycLDke3jZjjBzv_lb_RYl79Ozapwr17r7QymDR3aCHZLPetFTUcp3kWsyJAWAKMXz82bSJSlE=w959-h912"   # 환경우주탐험가
    ]

    headers = ["트렌드탐험대장", "모던스타일리스트", "그린스타일리스트", "환경우주탐험가"]  


    df = interact_with_gsheet('fetch', 'DB_설문조사', '응답', data=None) # action : fetch, append


    # '값' 열의 각 값에 대한 상대적 백분율 계산
    value_counts = pd.Series(df).value_counts(normalize=True) * 100

    # 결과를 딕셔너리 형태로 변환
    percentage_dict = value_counts.to_dict()

    # 결과 출력
    print(percentage_dict)

    for i, col in enumerate([col1, col2, col3, col4]):
        if headers[i] in percentage_dict.keys():
            percentage = percentage_dict[headers[i]]
        else : 
            percentage = 0
        with col:
            st.markdown(f"#### {headers[i]}")
            st.write(f"{percentage:.2f}%")
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center;">
                    <img src="{images[i]}" style="width: 100%; height: auto;">
                </div>
                """,
                unsafe_allow_html=True,
            )

def display_intro(): 
    st.markdown("# 옷BTI 설문조사")

    st.markdown(
             f"""
             <div style="display: flex; justify-content: center;">
                 <img src="https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihYbAHDhQFzSnos9bcXp2OKbXclhqtSG3dfEhZeWkSopDXDMDqhD9_vWxv9G5h9WqvaFLi-n15C4ydjrk-pYJf9wh1IsRlpATX8=w959-h912-rw-v1" style="width: 384px; height:384px; max-height: 24rem;">
             </div>
             """,
             unsafe_allow_html=True,
         )

    if st.button("찍찍이 유형 확인하기", key="start_survey"):
        st.session_state['page'] = 'survey'
        st.rerun()

def display_survey():
    set_page_style() 
    question_index = st.session_state.question_index
    if question_index < len(questions):
        question, options, image_url_survey = questions[question_index]

        st.markdown(f"## {question}")

        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <img src={image_url_survey} style="width: 288px; height: 288px;">
            </div>
            """,
            unsafe_allow_html=True,
        )

        for option in options:
            if st.button(option, key=f"{question_index}_{option}"):
                st.session_state.selected_options.append(option)
                time.sleep(0.2)  
                st.session_state.question_index += 1
                if st.session_state.question_index == len(questions):
                    st.session_state.page = 'results'
                st.rerun()

def display_results():
    st.markdown("## 설문 결과")

    selected_options = st.session_state.selected_options # 결과값 리스트

    result_data = list(selected_options)
    # 사용자의 선택에 대한 점수를 계산합니다.
    results = pd.Series(selected_options)
    converted_scores = results.map(score_dict).tolist()
    total_score = sum(converted_scores)

    # 총점수에 따라 결과 이미지와 메시지, 그리고 이미지 설명을 결정합니다.
    if total_score >= 30:
        image_url = "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihZVPtbjqbk6VO6nYUulBhzo9jMfw1Fe8CW8evIZKj2fYxSUzx-VGbZBkio5BHuEdOyfXHP-RMl0Le9Tv8KlogFXNTRBhs2O4w=w959-h912-rw-v1"
        message = "트렌드탐험대장"
        description_url = 'https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihbAz9m1QZeFS49dx_mg972RcvXmuo9zK3S-MCdwtJivoX1W3A5yIlHU7v-ev5jHw6r04VgqFp6ZIdr0XdLeCIFAILlM4WUNTGY=w959-h912-rw-v1'
    elif total_score >= 20:
        image_url = "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpiha5FhG-uc3zo3Qd8z3X8uwWzQw2cOO32sL2fJyQV6DXxZQgXiaWhueKptxiTOReMa1GffVniu7hnEpYUnLxrT5mCs84vk1-wFI=w959-h912-rw-v1"
        message = "모던스타일리스트"
        description_url = 'https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihbxYSAJLj7q1mdTR7KB6_Wfi_qyFsJKL_hHQeY40zD-V09emDrxLHe6X_SbhZzFrw0tIgZSocLQhdbeIk_S2ZGjDqHFNTRvYo0=w959-h912-rw-v1'
    elif total_score >= 10:
        image_url = "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpiha3SyI5t6muk9d9gQHZNv7mOooVaTTHRyo9DP8NW-zyh5kT4h1xszghHYcZIiPEytTKPvEN0xnYhz0Pj9CrmT3jfVajQOtuxQ=w959-h912-rw-v1"
        message = "그린스타일리스트"
        description_url = 'https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihZ5RFzdtIjQ8LZDOxea3FUfa7Nn9yp5Mmlm204k7zPns5iuSIjkCbomteVu765w_TYUrx1vCfC470Ahrt9KDKR7LIeo-HQ3sQ=w959-h912-rw-v1'
    else:
        image_url = "https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpiha4ebicanovZHhyCFdVZJL0LYycLDke3jZjjBzv_lb_RYl79Ozapwr17r7QymDR3aCHZLPetFTUcp3kWsyJAWAKMXz82bSJSlE=w959-h912"
        message = "환경우주탐험가"
        description_url = 'https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihak9xn8gfKkMBWk9PWFvx75COo05NtUkpBNstNIVGxwlx9Zwd6bdjrja9Q2eY6qdKLkA_CKTdknILLaccxMF7XW6IHIDBrYte8=w959-h912-rw-v1'

    
    if not st.session_state.get('results_saved', False):
         result_data.append(message)

         interact_with_gsheet('append', 'DB_설문조사', '응답', data=None)
         st.session_state['results_saved'] = True  # 결과가 저장되었다는 표시를 합니다.


    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <img src="{image_url}" style="width: 384px; height: 384px; max-height: 24rem;">
            <div style="text-align: center;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <a href="https://www.instagram.com/db_seoulsamgyetang/" target="_blank">
                <img src="{description_url}" style="width: 384px; height:384px; max-height: 24rem;">
            </a>
            <div style="text-align: center;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )



    # '다시 시작하기' 버튼을 제공하여 사용자가 설문조사를 재시작할 수 있도록 합니다.
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button('다시 시작하기'):
            st.session_state.page = 'cover'
            st.session_state.question_index = 0
            st.session_state.selected_options = []
            st.rerun()

def main():
    if st.session_state.page == 'cover':
        st.session_state['results_saved'] = False
        display_cover()
    elif st.session_state.page == 'intro': # 설명 페이지 추가
        display_intro()
    elif st.session_state.page == 'survey':
        display_survey()
    elif st.session_state.page == 'results':
        display_results()

if __name__ == "__main__":
    main()
