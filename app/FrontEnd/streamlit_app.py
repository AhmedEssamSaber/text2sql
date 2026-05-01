import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/api/chat"

st.set_page_config(page_title="Text2SQL Chat", layout="wide")

st.title("🧠 Text2SQL Chat")


# New Chat Button (هنا الإضافة)
col1, col2 = st.columns([1, 6])

with col1:
    if st.button("🔄 New Chat"):
        st.session_state.messages = []
        st.rerun()


# Session Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.info("💬 Start a new conversation...")


# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Input
user_input = st.chat_input("Ask your question...")

if user_input:

    # add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Generating..."):

        try:
            response = requests.post(
                API_URL,
                json={"messages": st.session_state.messages},
                timeout=30
            )

            if response.status_code != 200:
                st.error(f"Server Error: {response.text}")
                st.stop()

            data = response.json()

            if not data.get("success"):
                st.error("❌ Something went wrong from API")
                st.stop()

            sql = data.get("sql", "")
            result = data.get("result", [])
            explanation = data.get("explanation", "")

            
            # Assistant Message
            assistant_msg = f"```sql\n{sql}\n```"

            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_msg
            })

            with st.chat_message("assistant"):

                # SQL
                st.code(sql, language="sql")

                # Result
                if isinstance(result, list) and len(result) > 0:
                    df = pd.DataFrame(result)

                    row_count = len(df)

                    st.success(f"📊 Rows returned: {row_count}")

                    if "error" in df.columns:
                        st.error(df["error"].iloc[0])
                    else:
                        st.dataframe(df, use_container_width=True)
                else:
                    st.info("No results")

                # Explanation
                if explanation:
                    with st.expander("🧠 Explanation"):
                        st.write(explanation)

                # Meta
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("⏱ Time", f"{data.get('execution_time', 0)} sec")

                with col2:
                    st.metric("⚡ Cached", str(data.get("cached", False)))

        except requests.exceptions.Timeout:
            st.error("⏳ Request timed out")
        except Exception as e:
            st.error(f"❌ Error: {e}")