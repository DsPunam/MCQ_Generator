import os
import json
import pandas as pd 
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

#importing necessary libraries from langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain,SequentialChain

#load environment variables from the .env file
load_dotenv()

#Access the environment variables 
key=os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(openai_api_key=key,model_name='gpt-3.5-turbo',temperature=0.6)

template1="{text}.you have a text.now your task is to generate {number} mcq questions from this above text for {subject} student in {tone} tone.make sure that no mcq question is repeated and the questions are only from the above text.for generating mcq questions you have to follow the below response_json format.{response_json}"

quiz_generation_prompt1=PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=template1
)

quiz=LLMChain(llm=llm,prompt=quiz_generation_prompt1,output_key="quiz")

template2="You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.if the quiz is not at per with the cognitive and analytical abilities of the students,update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities. Quiz_MCQs:{quiz}"

correct_answer_generation_prompt2=PromptTemplate(
    input_variables=["subject","quiz"],
    template=template2
)

answer=LLMChain(llm=llm,prompt=correct_answer_generation_prompt2,output_key="review")

#overall chain
mcq_chain=SequentialChain(chains=[quiz,answer],input_variables=["text","number","subject","tone","response_json"],output_variables=["quiz","review"])


