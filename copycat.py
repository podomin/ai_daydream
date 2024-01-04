import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPEN_AI_KEY"]
)

st.title(" IF...지옥 🌋 만약에...지옥 💣")
st.markdown("#### N에 의한! N를 위한... 지피티와 함께하는 핑!퐁! 릴레이 망상")
st.markdown(" MBTI 'S'들은 눈 감아...그냥 지나가주세요")

st.success(" 원하는 망상에 대한 컨셉을 입력해주세요  ")
st.success(" 망상이어도 팩트체크를 하고 싶은 내용이 있다면 지피티백과 탭으로 이동!  ")


tab_liar, tab_dict = st.tabs(["망상", "지피티백과"])

with tab_liar:

    st.markdown("검색")
    auto_complete = st.toggle(label="예시로 채우기")
    example =  {
        "concept": "지구 상에서 바나나는 물론 바나나와 관련된 모든 것이 사라져버렸다. 유일하게 인공 바나나 감미료를 보유하고 있는 '반하나' 제과 회사가 계속 성장하기 위해 잡아야 할 방향성은? ",
        "genre" : "아포칼립스",
        "type" : "희망적",
        "feature" : "귀여움"
    }

    def generate_prompt(concept, genre, type, feature):
        prompt = f"""
    소설가의 입장에서 만약에 {concept} 에 대한 소설의 줄거리를 100자 이내로 생성해주세요. 
    해당 소설의 장르는 {genre}이고  {type}이고 그리고 {feature}이 있는 분위기의 소설이라는 점을 참고해주세요.
    최대한 상상력을 발휘해서 창의적으로 작성하세요.
    반드시 100자 이내로 작성해주세요.

    ---
    망상: {concept}
    장르: {genre}
    ---
        
        """.strip()
        return prompt


    def request_chat_completion(prompt):
        response = client.chat.completions.create(
            # model = "gpt-4-1106-preview",
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "당신은 창의적이고 상상력이 풍부한 소설가입니다."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        return response

    def print_streaming_response(response):
        message = ""
        placeholder = st.empty()
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content:
                message += delta.content
                placeholder.markdown(message + "▌")
        placeholder.markdown(message)
        

    with st.form("form_1"):
        concept = st.text_area(
                "컨셉을 적어주세요(필수)",
                value=example["concept"] if auto_complete else "",
                placeholder=example["concept"],
                height=10
                                )
        col1, col2, col3 = st.columns(3)
        with col1:
            genres = ['SF/과학', '판타지','청춘물', '히어로물',
                    '로맨스', '추리/미스터리',
                    '스릴러', '아포칼립스']
            genre = st.selectbox('장르 선택', genres)
            value=example["genre"] if auto_complete else "",
            placeholder=example["genre"]
            
        with col2:
            types = ['현실적','자극적', '희망적', '절망적']
            type = st.selectbox('특징 01 선택', types)
            value=example["type"] if auto_complete else "",
            placeholder=example["type"]
    
        with col3:
            features = ['교훈', '따뜻함','코믹함', '반전', '귀여움']
            feature = st.selectbox('특징 02 선택', features)
            value=example["feature"] if auto_complete else "",
            placeholder=example["feature"]
        
        submit = st.form_submit_button("제출하기")
        
    if submit:
        if not concept:
            st.error("컨셉을 입력해주세요.")
        elif not genre:
            st.error("장르를 선택해주세요.")
        elif not type:
            st.error("타입을 선택해주세요.")
        elif not feature:
            st.error("분위기를 선택해주세요.")
        else:
            prompt = generate_prompt(
                concept=concept,
                genre=genre,
                type=type,
                feature =feature,
            )
            response = request_chat_completion(prompt)
            print_streaming_response(response)
            

with tab_dict:            
        
    st.markdown("궁금한 내용을 검색해보세요")
    

    auto_complete = st.toggle(label="예시 보기")
    example =  {
        "question": "전 세계 바나나 소비량은?"
    }

    def generate_prompt(question):
        prompt = f"""
    {question} 질문에 대한 답을 작성해주세요. 반드시 100자 이상으로 작성해주세요.

    ---
    질문: {question}
    ---
        
        """.strip()
        return prompt

    def request_chat_completion(prompt):
        response = client.chat.completions.create(
            # model = "gpt-4-1106-preview",
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "당신은 최고의 검색 시스템입니다."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        return response

    def print_streaming_response(response):
        message = ""
        placeholder = st.empty()
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content:
                message += delta.content
                placeholder.markdown(message + "▌")
        placeholder.markdown(message)
        
    with st.form("form_2"):
        question = st.text_area(
                "궁금한 점 팩트 체크",
                value=example["question"] if auto_complete else "",
                placeholder=example["question"],
                height=5
                                )
        submit = st.form_submit_button("제출하기")
        
    if submit:
        if not question:
            st.error("질문을 작성해주세요.")
        else:
            prompt = generate_prompt(
                question = question
            )
            response = request_chat_completion(prompt)
            print_streaming_response(response)
            