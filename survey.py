import streamlit as st
from streamlit_gsheets import GSheetsConnection
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect
import random


st.set_page_config(
    page_title="Survey on LLM usage",
    page_icon="👩‍💻",
    layout="wide"
)

st.header("Survey on LLM usage")
st.markdown("****")
st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)    



# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
credentials = service_account.Credentials.from_service_account_info(
            st.secrets['connections']['gsheets'], 
            scopes=["https://www.googleapis.com/auth/spreadsheets",],)

url = "https://docs.google.com/spreadsheets/d/16iSrvR4XTyZNYg27Ud-ycnzGIX4xOtLepnBU_fysMp8/edit?gid=0#gid=0" # dataset

client=gspread.authorize(credentials)


def write_to_file(row, sheet_url):
    #sheet_url = collected_url #st.secrets["private_gsheets_url"] #this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).sheet1
    #sheet.append_row({"age": 'amanda', "gender": 'emanuele'})
    #body #the values should be a list
    sheet.append_row(row, table_range="A1:E1") 
    #st.success('Data has been written to Google Sheets')
    


### Defining state:
state = st.session_state

if 'PROLIFIC_PID' not in state:
    if st.query_params.to_dict():
        url_params = st.query_params.to_dict()
        annotator_id = url_params['PROLIFIC_PID']
        session_id = url_params['SESSION_ID']
    else:
        annotator_id = 'test'
        session_id = 'test'


if "form_filled" not in state:
    state.form_filled = False

########### DEMOGRAPHICS FORM ##############
placeholder = st.empty()
#if not state.form_filled:
with placeholder.container():
    with st.form("demographics"):
        st.subheader("Tell us a bit about you")

        gender = st.selectbox("Gender", ("Male", "Female", "Non-binary", "Prefer not to say"), index=None)
        
        age = st.radio('Age', ['18-24', '25-34' , '35-44', '45-54', '55-60', '60+'], None, key='_age', horizontal=True)

        nationality = st.selectbox('Nationality', options = ['United States', 'Canada', 'United Kingdom', 'Ireland', 'Australia', 'Other'], index = None)
 
        ethnicity = st.radio('What is your ethnicity?', options = ['American Indian or Alaskan Native', 'Asian / Pacific Islander', 'Black or African American', 'Hispanic', 'White / Caucasian', 'Multiple/Other. Please specify', 'Prefer not to say'],index = None, horizontal=True)
        ethn_free = st.text_input('If you selected other, please specify:', key = 'ethnic')

        marital = st.radio('What is your marital status?', options = ['Married', 'Cohabitating', 'Bereaved', 'Divorced', 'Single', 'Prefer not to say'], index=None, horizontal = True)
        
        language = st.selectbox('First language', index=None, options = ['English', 'Spanish', 'German', 'Chinese', 'French', 'Arabic', 'Other'])
        
        literacy = st.selectbox('Do you have a religious affiliation? If so, which one?', options = ['Christian', 'Muslim', 'Jewish', 'Other', 'None', 'Prefer not to say'], index = None)


        education = st.selectbox('Current education level', options = ['High school or below', 'Undergraduate degree', 'Graduate degree', 'Doctorate or above', 'Prefer not to say'], index=None)
        
        ses = st.radio('In terms of wealth, where would you place yourself in the socioeconomic ladder?', options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Prefer not to say'], index = None, horizontal = True)
        st.image("scale.png", caption="Macarthur scale", width = 350)
       
        home = st.radio("Do you own or rent your home?", ["Rent", "Own", "Prefer not to say"], index=None, horizontal=True)

        employment_options = ['Employed full time', 'Employed part time', 'Self-employed full time', 'Self-employed part time', 'Not employed, but looking for work',
                                'Not employed and not looking for work', 'Not employed, unable to work due to a disability or illness', 'Retired', 
                                'Student', 'Stay-at-home spouse or partner']
        employment = st.selectbox('What is your current employment status?', options = employment_options, index=None)
        mum_education = st.selectbox('What was the highest level of education achieved by your mother?', options = ['High school or below', 'Undergraduate degree', 'Graduate degree', 'Doctorate or above', 'Prefer not to say'], index=None)
        dad_education = st.selectbox('What was the highest level of education achieved by your father?', options = ['High school or below', 'Undergraduate degree', 'Graduate degree', 'Doctorate or above', 'Prefer not to say'], index=None)

        list_hobbies = ["Listen to jazz", "Listen to classical music", "Listen to rock/indie music", "Listen to hiphop and rap", "Go to gigs", 
                        "Go to the opera", "Visit to stately homes", "Exercise", "Use social media", "Go to museums and galleries", 
                        "Do arts and crafts", "Watch dance or ballet", "Attend football matches", "Watch sports", "Watch dance or ballet", "Other"]
        hobbies = st.multiselect("What sorts of things do you do in your free time? You may select more than one.", list_hobbies)

        
        st.markdown('***')

        instructions = ''' The next set of questions regard your use of technology. Read the definition for "language technology" below: \n 
                            Language technology refers to any piece of software that is intended to assist humans with language specific tasks in a technological setting 
                            (i.e., on a mobile phone, tablet, computer, the internet, smart devices). 
                            Some examples of language technologies include: 
                            Spell checkers in e-mail helps people to write more professional e-mails; 
                            Google Translate helps people to translate text from one language to another; 
                            internet search engines (e.g. Google, Bing, Yahoo) help people to find websites relevant to a given query.

                        '''

        st.write(instructions)

        tech = st.multiselect('Which digital technologies do you have access to on a daily basis? Select all that apply.', options = ['Laptop', 'Smartphone', 'Tablet', 'Smartwatch', 'Other'])
        tech_other = st.text_input("If you selected 'Other', please specify which:", key = 'tech')



        nlp = ['Spell checker (i.e., correcting misspellings)', 'Grammar checker (i.e., correcting grammar mistakes)', 'E-mail spam detection (i.e., automatically send spam e-mails to your Trash folder)',
                'Sentiment analysis (e.g. automatically detect if user reviews are positive or negative)'
                'Machine translation (e.g. translate Chinese or Russian into English, and vice versa)',
                'Paraphrasing and Summarisation (i.e., automatically produce alternative descriptions of written text)',
                'Question Answering & Search Engine. (e.g., browsers or ask questions to smart devices/assistants)',
                'Dialog technology (e.g. chatbots that communicate with you)',
                'Speech-to-Text (i.e. a computer transcribing your spoken language to written language)',
                'Text-to-Speech (i.e, computers being able to read out loud written language)',
                 'Reading text from scanned documents (i.e. “Optical character recognition” or OCR. Given an image representing printed text, determine the corresponding text.)']


        tasks = [
            "Coding",
            "Translation",
            "Brainstorming",
            "Writing (e.g., composing emails)",
            "Paraphrasing or finding synonyms",
            "Proofreading/Editing (e.g., grammar, spelling, structure improvements)",
            "Digital content creation (e.g., creation of social media content)",
            "Generic chatbot conversation",
            "Solving math or logical problems",
            "Analyze data",
            "Generate art",
            "Play games",
            "Completing assignments",
            "Learning (e.g., explaining complex concepts in simple terms)",
            "Get information about current events",
            "Answering questions about general knowledge",
            "Collecting references",
            "Summarizing long texts",
            "Other (specify)"
        ]


        llms = ['Character.AI', 'ChatGPT', 'Claude', 'GitHub Copilot', 'Google Bard', 'Google Gemini', 'Grok', 'HuggingChat', 'Jasper', 'Meta Llama 2', 'Microsoft Bing AI', 'Pi', 'Poe', 'Perplexity', 'Snapchat My AI', 'Other', 'None of these']

        
        know_nlp = st.multiselect("Which of the following language technologies have you heard about?", nlp)
        know_other = st.text_input("If you selected 'Other', please specify which:", key = 'know')

        use_nlp = st.multiselect("Which of the following language technologies have you used?", nlp)
        use_nlp_other = st.text_input("If you selected 'Other', please specify which:", key = 'use_nlp')

        would_nlp = st.multiselect("Below is a list of some common language technologies. Please check every one that you would find useful, but do not use because of scarce performance", nlp)
        would_other = st.text_input("If you selected 'Other', please specify which:", key = 'would')


        use_ai = st.select_slider("How often do you use AI chatbots like chatGPT?", options=["Every day", "Nearly every day", "Sometimes", "Rarely", "Never"], value = None)
        #ai_other = st.text_input("If you selected 'Other', please specify which:", key = 'ai')


        llm_use = st.multiselect('Which of these AI chatbots do you use?', llms)

        llm_other = st.text_input("If you selected 'Other', please specify which:", key = 'llms')
        
        usecases = st.multiselect("Have you ever used ChatGPT (or other similar chatbots) for any of the following? You can select multiple.", tasks)
        
        use_other = st.text_input("If you selected 'Other', please specify which:", key = 'use')

        contexts = st.multiselect("In which of the following contexts have you ever used ChatGPT (or other similar chatbots)? ", ['Work', 'School/University', 'Entertainment', 'Learning', 'Personal', 'Creative or artistic', 'Technical', 'Other (specify)'])

        st.write("Next, we want to know more about the sorts of things you use AI for. Note that this form is anonymous -- we will not associate this information with your prolific ID.")

        prompts = st.text_area(label='Provide us with the last ten prompts you used for your chosen AI chatbot. One prompt per line with a semicolon after the prompt:')
        
        comments = st.text_area(label='Do you have any other comments?')

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")#, on_click=populate_annotations)
        if submitted:
            #if not gender or not age or not nationality or not language or not education or not literacy or not use_ai:
            #    st.warning("Please complete the form")
            #else:
            write_to_file([annotator_id, session_id, gender, age, nationality, language, ethnicity, ethn_free, marital, language, literacy, education, ses, home, employment, mum_education, dad_education, ''.join(hobbies), ''.join(tech), tech_other, ''.join(know_nlp), ''.join(use_nlp), ''.join(would_nlp), ''.join(use_ai), know_other, use_nlp_other, would_other, ''.join(llm_use), llm_other, ''.join(usecases), use_other, ''.join(contexts),  prompts, comments], url)
            placeholder.empty()
            state.form_filled = True



if state.form_filled:
    with open('codes') as f:
        lines = f.read().splitlines()
        code = random.choice(lines)
        st.subheader("Thank you!")
        st.write("Thank you very much for completing the task. You can now return to Prolific and enter the code **{}**.".format(code))