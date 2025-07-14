import pandas as pd
import streamlit as st
from utils import dataframe_agent
import plotly.express as px

def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    if chart_type == "bar":
        df_data.set_index(input_data["columns"][0], inplace=True)
        st.bar_chart(df_data)
    elif chart_type == "line":
        df_data.set_index(input_data["columns"][0], inplace=True)
        st.line_chart(df_data)
    elif chart_type == "scatter":
        if len(input_data["columns"]) >= 2:
            fig = px.scatter(df_data, x=input_data["columns"][0], y=input_data["columns"][1])
            st.plotly_chart(fig)
        else:
            st.write("散点图需要至少两列数据")
st.title("💡 CSV数据分析智能工具")

with st.sidebar:
    api_key = st.text_input("请输入DeepSeek API密钥:", type="password")
    st.markdown("[获取DeepSeek API密钥](https://platform.deepseek.com)")

data = st.file_uploader("上传你的数据文件（CSV格式）：", type="csv")

if data:
    df = pd.read_csv(data)
    st.session_state["df"] = df
    with st.expander("原始数据"):
        st.dataframe(df)

query = st.text_area("请输入你关于以上表格的问题，或数据提取请求，或可视化要求（支持散点图、折线图、条形图）：")

if st.button("生成回答"):
    if not api_key:
        st.info("请输入你的DeepSeek API密钥")
    elif "df" not in st.session_state:
        st.info("请先上传数据文件")
    else:
        with st.spinner("正在思考中，请稍候..."):
            response_dict = dataframe_agent(api_key, st.session_state["df"], query)
            if "answer" in response_dict:
                st.write(response_dict["answer"])
            if "table" in response_dict:
                st.table(pd.DataFrame(response_dict["table"]["data"], columns=response_dict["table"]["columns"]))
            if "bar" in response_dict:
                create_chart(response_dict["bar"], "bar")
            if "line" in response_dict:
                create_chart(response_dict["line"], "line")
            if "scatter" in response_dict:
                create_chart(response_dict["scatter"], "scatter")