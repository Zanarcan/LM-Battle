import streamlit as st

st.title("Test Minimal")
st.write("Si ves esto, Streamlit funciona")

if st.button("Test Button"):
    st.success("Button works!")
