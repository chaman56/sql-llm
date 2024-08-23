from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response
# C:\Users\ycham\AppData\Local\Programs\Python\Python312\python.exe C:\msys64\mingw64\bin\python.exe
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    heads = []
    if cur.description:
        heads = [col[0] for col in cur.description]
    print(heads)
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return (heads,rows)

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION, MARKS \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    keep in mind that there is only one table student and output only SQL commands nothing else.
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.chat_input("Ask your question! ")

if question:
    with st.chat_message("user"):
        st.markdown(question)
    response=get_gemini_response(question,prompt)
    print(response)
    st.code(response, language='sql')
    heads,response=read_sql_query(response,r"C:\Users\ycham\OneDrive\Desktop\WorkSpace\student.db")
    st.subheader("The Response is")
    st.text(heads)
    for row in response:
        print(row)
        st.write(row)



# def generate_content(question):
#     model=genai.GenerativeModel('gemini-pro')
#     response=model.generate_content(question)
#     return response.text

# if 'chats' not in st.session_state:
#     st.session_state['chats'] = []

# for message in st.session_state.chats:
#     with st.chat_message(message[0]):
#         st.markdown(message[1])

# if question:
#     st.session_state.chats.append(("user",question))
#     with st.chat_message("user"):
#         st.markdown(question)
#     response = generate_content(question)
#     st.session_state.chats.append(("AI",response))
#     with st.chat_message("AI"):
#         st.markdown(response)








