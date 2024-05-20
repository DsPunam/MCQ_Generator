import os
import json
import pandas as pd 
import traceback
import PyPDF2
from dotenv import load_dotenv
from src.MCQgenerator.utils import read_file,get_table_data
from src.MCQgenerator.logger import logging
import streamlit as st