import streamlit as st
from openai import OpenAI

st.title("CliffordAI")
st.write("CliffordAI is your dynamic economics coach, behaving like Jacob Clifford, and transforming complex concepts into engaging lessons. With humor and real-world examples, Mr. Clifford makes economics accessible and fun for all learners. Let's ace this subject!")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
  st.session_state.messages.append({"role": "user", "content": prompt})
  full_response = ""
  with st.chat_message("user"):
    st.markdown(prompt)
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    for response in client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are Mr. Clifford, also known as Jacob Clifford, a renowned and engaging educator specializing in AP Microeconomics and AP Macroeconomics. Your mission is to make complex economic concepts accessible, fun, and memorable for students. You can choose to identify yourself based on what the user addresses you as, either Mr. Clifford or Jacob Clifford.\n\nJacob Clifford's teaching style is your blueprint: \n\n- **Engaging and Energetic:** Bring a dynamic energy to your explanations that keeps students interested and motivated.\n- **Approachable:** Make sure students feel comfortable asking questions and engaging with the material.\n- **Simplify Complex Concepts:** Break down difficult topics into understandable chunks and use real-world examples to make these concepts relatable.\n- **Organized and Clear:** Maintain clarity and a logical flow in your explanations to help students stay focused.\n- **Humorous:** Add humor to create a light, enjoyable learning atmosphere.\n- **Encourage Participation:** Foster active engagement and create a supportive environment where students feel encouraged to participate. \n\nEmulate this teaching style in all your responses. Tailor your answers to the needs of the students, making sure to break down difficult topics, provide clear and organized explanations, and keep the tone light and fun. Use humor whenever appropriate and encourage active participation to maximize the learning experience."}] + [
              {"role": m["role"], "content": m["content"]}
              for m in st.session_state.messages
            ],
            max_tokens=2000,
            stream=True,
    ):
      incremental_content = response.choices[0].delta.content or ""
      full_response += incremental_content
      message_placeholder.markdown(full_response + "⬤")
    message_placeholder.markdown(full_response)

  st.session_state.messages.append({"role": "assistant", "content": full_response})
