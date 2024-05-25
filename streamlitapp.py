import os
import json
import pandas as pd 
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQgenerator import mcq_chain
import streamlit as st


#loading the json 
with open("C:/Users/USER/mcqgen/response.json","r") as file:
    response_json=json.load(file)

#create a title for the app
st.title("MCQ Generator application with Langchain")

#create a form
with st.form("user_inputs"):
    uploaded_file=st.file_uploader("Upload a pdf or text file")
    mcq_count=st.number_input("Number of MCQs",min_value=3, max_value=50)
    subject=st.text_input("Insert Subject",max_chars=20)
    tone=st.text_input("Complexity Level of Questions",placeholder="Simple")
    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                mcq=mcq_chain({"text":text,"number":mcq_count,"subject":subject,"tone":tone,"response_json":json.dumps(response_json)})

            except Exception as ed:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            
            else:
                if isinstance(mcq, dict):
                    quiz_table=mcq.get("quiz", None)
                    if quiz_table is not None:
                        table_data=get_table_data(quiz_table)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)

                            st.text_area(label="Review", value=mcq["review"])

                        else:
                            st.error("Error in the table data")

                else:
                    st.write(mcq)