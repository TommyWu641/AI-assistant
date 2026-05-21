import streamlit as st
import os
from openai import OpenAI
import json
from datetime import datetime
system_prompt = ("""你的名字叫%s，你现在是用户的助手
你需要：
    匹配用户语言
    回复的内容要体现助手特征
    回复要简短
    性格特征：
        %s
        
""")

# Object notation

def save_session():
    if st.session_state.current_session:
        session_data={
            "nickname":st.session_state.nickname,
            "nature":st.session_state.nature,
            "messages":st.session_state.messages,
            "current_session":st.session_state.current_session
        }
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        with open(f"sessions/{st.session_state.current_session}.json","w",encoding="utf-8") as f:
            json.dump(session_data,f,ensure_ascii=False,indent = 2)
st.set_page_config(
    page_title="AI 智能助手",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={

    }
)
def load_sessions():
    session_list = []
    #加载sessions目录下面的所有文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5:1])
    return session_list

def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json","r",encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages= session_data["messages"]
                st.session_state.nickname = session_data["nickname"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error("加载会话信息失败")
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            if session_name == st.session_state.current_session:
                st.session_state.current_session = datetime.now().strftime("%Y%m%d%H%M%S")
                st.session_state.messages = []
    except Exception:
        st.error("删除会话信息失败")

st.title("AI 智能助手")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "nickname" not in st.session_state:
    st.session_state.nickname = "云兔球"
if "nature" not in st.session_state:
    st.session_state.nature = "广东本地人"
if "current_session" not in st.session_state:
    st.session_state.current_session = datetime.now().strftime("%Y%m%d%H%M%S")
st.text(f"会话名称：{st.session_state.current_session}")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

if st.sidebar.button("新建会话",width="stretch",icon="🐽"):
    save_session()
    if st.session_state.messages:
        st.session_state.messages=[]
        st.session_state.current_session = datetime.now().strftime("%Y%m%d%H%M%S")
        save_session()
        st.rerun()
#会话历史
with st.sidebar:
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([3,1])
        with col1:
           if st.button(session,width="stretch",key=f"load{session}",icon="💻️",type="primary" if session == st.session_state.current_session else "secondary"):
               load_session(session)
               st.rerun()
        with col2:
            if st.button("",width="stretch",key=f"delete{session}",icon="🗑️"):
                delete_session(session)


st.sidebar.subheader("助手信息")
nickname = st.sidebar.text_input("助手名称",placeholder="请输入助手的昵称",value=st.session_state.nickname)
if nickname:
    st.session_state.nickname = nickname
nature = st.sidebar.text_area("助手性格",placeholder="请输入助手性格",value = st.session_state.nature)
if nature:
    st.session_state.nature = nature
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

prompt = st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print(f"--------调用了AI大模型，调试词是：{prompt}")

    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nickname,st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    # print("AI大模型的输出结果：",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)
    response_message = st.empty()
    full_response=""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_session()