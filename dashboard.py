import streamlit as st
import pandas as pd

st.title("LinkedIn Post Performance & Audience Analysis")

st.header("Post Features")
post_df = pd.read_csv("post_features.csv")
st.dataframe(post_df)

st.header("Audience Relevance")
audience_df = pd.read_csv("audience_analysis.csv")
st.dataframe(audience_df)
