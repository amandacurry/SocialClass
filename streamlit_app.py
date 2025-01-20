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

url = "https://docs.google.com/spreadsheets/d/1mHD3UA-zf6zSgChM8pQn1E7SENIGmBzxvXq-quFNImg/edit?usp=sharing" # dataset

client=gspread.authorize(credentials)

countries = ['United States', 'United Kingdom', 'China', 'Canada', 'United Arab Emirates', 'Australia', 'Andorra', 'Afghanistan', 'Antigua and Barbuda', 'Anguilla', 'Albania', 'Armenia', 'Angola', 'Antarctica', 'Argentina', 'American Samoa', 'Austria', 'Aruba', 'Azerbaijan', 'Bosnia and Herzegovina', 'Barbados', 'Bangladesh', 'Belgium', 'Burkina Faso', 'Bulgaria', 'Bahrain', 'Burundi', 'Benin', 'Saint Barthelemy', 'Bermuda', 'Brunei', 'Bolivia', 'Brazil', 'Bahamas, The', 'Bhutan', 'Bouvet Island', 'Botswana', 'Belarus', 'Belize', 'Cocos (Keeling) Islands', 'Congo, Democratic Republic of the', 'Central African Republic', 'Congo, Republic of the', 'Switzerland', 'Cote d\'Ivoire', 'Cook Islands', 'Chile', 'Cameroon', 'Colombia', 'Costa Rica', 'Cuba', 'Cape Verde', 'Curacao', 'Christmas Island', 'Cyprus', 'Czech Republic', 'Germany', 'Djibouti', 'Denmark', 'Dominica', 'Dominican Republic', 'Algeria', 'Ecuador', 'Estonia', 'Egypt', 'Western Sahara', 'Eritrea', 'Spain', 'Ethiopia', 'Finland', 'Fiji', 'Falkland Islands (Islas Malvinas)', 'Micronesia, Federated States of', 'Faroe Islands', 'France', 'France, Metropolitan', 'Gabon', 'Grenada', 'Georgia', 'French Guiana', 'Guernsey', 'Ghana', 'Gibraltar', 'Greenland', 'Gambia, The', 'Guinea', 'Guadeloupe', 'Equatorial Guinea', 'Greece', 'South Georgia and the Islands', 'Guatemala', 'Guam', 'Guinea-Bissau', 'Guyana', 'Hong Kong (SAR China)', 'Heard Island and McDonald Islands', 'Honduras', 'Croatia', 'Haiti', 'Hungary', 'Indonesia', 'Ireland', 'Israel', 'Isle of Man', 'India', 'British Indian Ocean Territory', 'Iraq', 'Iran', 'Iceland', 'Italy', 'Jersey', 'Jamaica', 'Jordan', 'Japan', 'Kenya', 'Kyrgyzstan', 'Cambodia', 'Kiribati', 'Comoros', 'Saint Kitts and Nevis', 'Korea, South', 'Kuwait', 'Cayman Islands', 'Kazakhstan', 'Laos', 'Lebanon', 'Saint Lucia', 'Liechtenstein', 'Sri Lanka', 'Liberia', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Libya', 'Morocco', 'Monaco', 'Moldova', 'Montenegro', 'Saint Martin', 'Madagascar', 'Marshall Islands', 'Macedonia', 'Mali', 'Burma', 'Mongolia', 'Macau (SAR China)', 'Northern Mariana Islands', 'Martinique', 'Mauritania', 'Montserrat', 'Malta', 'Mauritius', 'Maldives', 'Malawi', 'Mexico', 'Malaysia', 'Mozambique', 'Namibia', 'New Caledonia', 'Niger', 'Norfolk Island', 'Nigeria', 'Nicaragua', 'Netherlands', 'Norway', 'Nepal', 'Nauru', 'Niue', 'New Zealand', 'Oman', 'Panama', 'Peru', 'French Polynesia', 'Papua New Guinea', 'Philippines', 'Pakistan', 'Poland', 'Saint Pierre and Miquelon', 'Pitcairn Islands', 'Puerto Rico', 'Gaza Strip', 'West Bank', 'Portugal', 'Palau', 'Paraguay', 'Qatar', 'Reunion', 'Romania', 'Serbia', 'Russia', 'Rwanda', 'Saudi Arabia', 'Solomon Islands', 'Seychelles', 'Sudan', 'Sweden', 'Singapore', 'Saint Helena, Ascension, and Tristan da Cunha', 'Slovenia', 'Svalbard', 'Slovakia', 'Sierra Leone', 'San Marino', 'Senegal', 'Somalia', 'Suriname', 'South Sudan', 'Sao Tome and Principe', 'El Salvador', 'Sint Maarten', 'Syria', 'Swaziland', 'Turks and Caicos Islands', 'Chad', 'French Southern and Antarctic Lands', 'Togo', 'Thailand', 'Tajikistan', 'Tokelau', 'Timor-Leste', 'Turkmenistan', 'Tunisia', 'Tonga', 'Turkey', 'Trinidad and Tobago', 'Tuvalu', 'Taiwan, Province of China', 'Tanzania', 'Ukraine', 'Uganda', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Holy See (Vatican City)', 'Saint Vincent and the Grenadines', 'Venezuela', 'British Virgin Islands', 'Virgin Islands', 'Vietnam', 'Vanuatu', 'Wallis and Futuna', 'Samoa', 'Kosovo', 'Yemen', 'Mayotte', 'South Africa', 'Zambia', 'Zimbabwe']
def write_to_file(row, sheet_url):
    #sheet_url = collected_url #st.secrets["private_gsheets_url"] #this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).sheet1
    sheet.append_row(row, table_range="A1:Z1") 
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

        st.write('We are conducting research about the ways in which people of all backgrounds are using AI. To understand if there are differences in the ways different people are using AI chatbots and other technologies, we are running a survey. ')
        st.write('Any data published will be fully anonymised. ')
        st.write('USE TAB TO GO TO THE NEXT SECTION. DO NOT PRESS ENTER TO MOVE TO THE NEXT SECTION OR THE FORM WILL SUBMIT!!!')

        jobs = ['Manager or business owner (those who plan, direct, coordinate and evaluate the overall activities of enterprises, governments and other organizations)', 'Professionals or highly skilled workers (those who increase the existing stock of knowledge or teach about it in a systematic manner, e.g. engineer, doctor, teacher, lawyer)', 'Technicians and associate professionals (those who apply scientific or artistic concepts and operational methods, e.g. secretaries, fitness workers, lab technicians)', 'Clerical support workers (those who perform clerical duties such as organizing, storing, computing and retrieving information)',
                'Service and sales workers (whose who provide personal and protective services related to travel, housekeeping, catering, personal care, protection against fire and unlawful acts; or sell goods)', 'Skilled agricultural, forestry and fishery workers (those harvest, grow, breed, or produce a variety of animal husbandry products)', 'Craft related trades workers (those who produce or process foodstuffs, textiles, wooden, metal and other articles, including handicraft goods, and apply specific technical and practical knowledge and skills to construct and maintain buildings)', 
                'Plant and machine operators, and assemblers (those who maintain, operate and monitor industrial and agricultural machinery and equipment)', 'Elementary occupations (jobs that involve simple and routine tasks which may require the use of hand-held tools and considerable physical effort)', 'Armed forces occupations (includes all jobs held by members of the armed forces)', 'Homemaker', 'Prefer not to say']
        
        placeholder_s = "Select all that apply."

        gender = st.selectbox("Gender*", ("Male", "Female", "Non-binary", "Other, please specify.", "Prefer not to say"), index=None)

        gender_other = st.text_input('If you selected other, please specify:', key = 'gender')
        
        age = st.radio('Age*', ['18-24', '25-34' , '35-44', '45-54', '55-60', '60+'], None, key='_age', horizontal=True)

        nationality = st.multiselect('Nationality (You may select multiple):*', options = countries, placeholder=placeholder_s)
 
        ethnicity = st.multiselect('What is your ethnicity? You may select more than one.*', options = ['American Indian or Alaskan Native', 'Asian / Pacific Islander', 'Black or African American', 'Hispanic', 'White / Caucasian', 'Other. Please specify', 'Prefer not to say'], placeholder=placeholder_s)
        ethn_free = st.text_input('If you selected other, please specify:', key = 'ethnic')

        marital = st.radio('What is your marital status?*', options = ['Married', 'Cohabitating', 'Bereaved', 'Divorced', 'Single', 'Other (Please Specify)', 'Prefer not to say'], index=None, horizontal = True)
        marital_free = st.text_input('If you selected other, please specify:', key = 'mar')

        language = st.multiselect('What is your first language? You may select more than one, if applicable.*', options = ['English', 'Spanish', 'German', 'Chinese', 'French', 'Arabic', 'Other (Please Specify)'], placeholder=placeholder_s)
        language_free = st.text_input('If you selected other, please specify:', key = 'lang')

        religion = st.selectbox('Do you have a religious affiliation? If so, which one?*', options = ['Christian', 'Muslim', 'Jewish',  'Buddhist', 'Other, please specify.', 'None', 'Prefer not to say'], index = None)
        religion_other = st.text_input('If you selected other, please specify:', key = 'religion')

        education = st.selectbox('Current education level* ', options = ['High school or below', 'Undergraduate degree', 'Graduate degree', 'Doctorate or above', 'Prefer not to say'], index=None)
        mum_education = st.selectbox('What was the highest level of education achieved by your mother?*', options = ['High school or below', 'Undergraduate degree', 'Graduate degree', 'Doctorate or above', 'Prefer not to say'], index=None)
        dad_education = st.selectbox('What was the highest level of education achieved by your father?*', options = ['High school or below', 'Undergraduate degree', 'Graduate degree', 'Doctorate or above', 'Prefer not to say'], index=None)

        ses = st.radio('Based on the picture below, where would you place yourself in the socioeconomic ladder in terms of wealth?*', options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Prefer not to say'], index = None, horizontal = True)
        st.image("scale.png", caption="Macarthur scale", width = 350)
       
        home = st.radio("Do you own or rent your home?*", ["Rent", "Own", "Other (Please specify)", "Prefer not to say"], index=None, horizontal=True)
        home_free = st.text_input('If you selected other, please specify:', key = 'home_free')
        employment_options = ['Employed full time', 'Employed part time', 'Self-employed full time', 'Self-employed part time', 'Not employed, but looking for work',
                                'Not employed and not looking for work', 'Not employed, unable to work due to a disability or illness', 'Retired', 
                                'Student', 'Stay-at-home spouse or partner', 'Prefer not to say']
        
        employment = st.selectbox('What is your current employment status?*', index=None, options = employment_options)
        self_emplo = st.multiselect("What is/was your current occupation? You may select more than one.*", options = jobs, placeholder=placeholder_s)
        mother_occ = st.multiselect("What is/was your mother's occupation? You may select more than one.*", options = jobs, placeholder=placeholder_s)
        father_occ = st.multiselect("What is/was your father's occupation? You may select more than one.*", options = jobs, placeholder=placeholder_s)


        list_hobbies = ["Listen to jazz", "Listen to classical music", "Listen to rock/indie music", "Listen to hiphop and rap", "Go to gigs", 
                        "Go to the opera", "Visit to stately homes", "Exercise", "Use social media", "Go to museums and galleries", 
                        "Do arts and crafts", "Watch dance or ballet", "Attend football matches", "Watch sports", "Other (Please specify)"]
        hobbies = st.multiselect("What sorts of things do you do in your free time? You may select more than one.*", list_hobbies, placeholder=placeholder_s)
        hobbies_other = st.text_input('If you selected other, please specify:', key = 'hobbies')

        

        
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

        tech = st.multiselect('Which digital technologies do you have access to on a daily basis? Select all that apply.*', placeholder=placeholder_s, options = ['Laptop', 'Smartphone', 'Tablet', 'Smartwatch', 'Other'])
        tech_other = st.text_input("If you selected 'Other', please specify which:", key = 'tech')



        nlp = ['Spell checker (i.e., correcting misspellings)', 'Grammar checker (i.e., correcting grammar mistakes)', 'E-mail spam detection (i.e., automatically send spam e-mails to your Trash folder)',
                'Sentiment analysis (e.g. automatically detect if user reviews are positive or negative)'
                'Machine translation (e.g. translate Chinese or Russian into English, and vice versa)',
                'Paraphrasing and Summarisation (i.e., automatically produce alternative descriptions of written text)',
                'Question Answering & Search Engine. (e.g., browsers or ask questions to smart devices/assistants)',
                'Dialog technology (e.g. chatbots that communicate with you such as chatGPT)',
                'Speech-to-Text (i.e. a computer transcribing your spoken language to written language)',
                'Text-to-Speech (i.e, computers being able to read out loud written language)',
                 'Reading text from scanned documents (i.e. “Optical character recognition” or OCR. Given an image representing printed text, determine the corresponding text.)', 'Other (specify)']


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

        
        know_nlp = st.multiselect("Which of the following language technologies have you heard about?*", nlp, placeholder=placeholder_s)
        know_other = st.text_input("If you selected 'Other', please specify which:", key = 'know')

        use_nlp = st.multiselect("Which of the following language technologies have you used?*", nlp, placeholder=placeholder_s)
        use_nlp_other = st.text_input("If you selected 'Other', please specify which:", key = 'use_nlp')

        would_nlp = st.multiselect("Below is a list of some common language technologies. Please check every one that you would find useful, but do not use because of scarce performance*", nlp, placeholder=placeholder_s)
        would_other = st.text_input("If you selected 'Other', please specify which:", key = 'would')


        use_ai = st.select_slider("How often do you use AI chatbots like chatGPT?*", options=["Every day", "Nearly every day", "Sometimes", "Rarely", "Never"], value = None)
        #ai_other = st.text_input("If you selected 'Other', please specify which:", key = 'ai')


        llm_use = st.multiselect('If you use them, which of these AI chatbots do you use? If you have never used them, leave blank.', llms, placeholder=placeholder_s)

        llm_other = st.text_input("If you selected 'Other', please specify which:", key = 'llms')
        
        usecases = st.multiselect("If you have used AI chatbots, have you ever them for any of the following? You can select multiple. If you have never used them, leave blank.", tasks, placeholder=placeholder_s)
        
        use_other = st.text_input("If you selected 'Other', please specify which:", key = 'use')

        contexts = st.multiselect("In which of the following contexts have you ever used ChatGPT (or other similar chatbots)? If you have never used them, leave blank.", ['Work', 'School/University', 'Entertainment', 'Learning', 'Personal', 'Creative or artistic', 'Technical', 'Other (specify)'], placeholder=placeholder_s)
        contexts_other = st.text_input("If you selected 'Other', please specify which:", key = 'context')
        st.write("Next, we want to know more about the sorts of things you use AI for. Note that this form is anonymous -- we will not associate this information with your prolific ID. If you have never used them, leave blank.")


        st.write('If you can, please provide us with the last ten questions or requests you used for your chosen AI chatbot. Preferably, copy and paste the questions directly from the conversation. You will receive a bonus for each additional prompt you provide. Responses will be manually checked. ')
        st.write('USE TAB TO GO TO THE NEXT SECTION. DO NOT PRESS ENTER TO MOVE TO THE NEXT FIELD OR THE FORM WILL SUBMIT!!!')
        prompt1 = st.text_input("Prompt:*", key = 'p1')
        prompt2 = st.text_input("Prompt*", key = 'p2')
        prompt3 = st.text_input("Prompt*", key = 'p3')
        prompt4 = st.text_input("Prompt*", key = 'p4')
        prompt5 = st.text_input("Prompt*", key = 'p5')
        prompt6 = st.text_input("Prompt", key = 'p6')
        prompt7 = st.text_input("Prompt", key = 'p7')
        prompt8 = st.text_input("Prompt", key = 'p8')
        prompt9 = st.text_input("Prompt", key = 'p9')
        prompt10 = st.text_input("Prompt", key = 'p10')

        comments = st.text_area(label='Do you have any other comments, about this survey or about AI chatbots?')

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")#, on_click=populate_annotations)
        if submitted:
            all_valid = True
            required = [gender]#, age, nationality, language, ethnicity, marital,  language,  religion,  education, ses, home,  mum_education, dad_education, employment, self_emplo, mother_occ, father_occ, hobbies,  tech, know_nlp, use_nlp, would_nlp, use_ai]
            cond = [llm_use, usecases, contexts,  prompt1, prompt2, prompt3, prompt4, prompt5, prompt6, prompt7, prompt8, prompt9, prompt10]

            if any(field is None or field == "" for field in required):
                st.warning("Please complete all required fields in the form.")
                all_valid = False



            # Check AI-specific conditions
            if use_ai == "Never" and any(cond):
                st.warning("Only complete these sections if you have used AI chatbots.")
                all_valid = False
            elif use_ai in ["Every day", "Nearly every day"]:
                # Check additional required fields for frequent AI users
                ai_required = [llm_use, usecases, contexts]
                prompts = [prompt1, prompt2, prompt3, prompt4, prompt5]
                if any(field is None or field == [] for field in ai_required):
                    st.warning("Please fill in the sections about your use of AI.")
                    all_valid = False
                # Check for at least 5 prompts
                elif any(prompt is None or prompt.strip() == "" for prompt in prompts):
                    st.write(llm_use)
                    st.warning("Please provide at least five prompts. You will receive a bonus for each additional answer. Responses will be manually checked.")
                    all_valid = False

            # Proceed if all validations pass
            if all_valid:
                demographic_information = [
                    gender, gender_other, age, ';'.join(nationality), ';'.join(ethnicity), ethn_free,
                    marital, marital_free, ';'.join(language), language_free, religion, religion_other, 
                    education, mum_education, dad_education, ses, home, home_free, employment, 
                    ';'.join(self_emplo), ';'.join(mother_occ), ';'.join(father_occ), ';'.join(hobbies), hobbies_other
                ]
                tech_information = [
                    ';'.join(tech), tech_other, ';'.join(know_nlp), know_other, ';'.join(use_nlp), 
                    use_nlp_other, ';'.join(would_nlp), would_other, use_ai, ';'.join(llm_use), 
                    llm_other, ';'.join(usecases), use_other, ';'.join(contexts), contexts_other
                ]
                row = [annotator_id, session_id] + demographic_information + tech_information + [
                    prompt1, prompt2, prompt3, prompt4, prompt5, prompt6, prompt7, prompt8, prompt9, prompt10, comments
                ]
                write_to_file(row, url)
                #placeholder.empty()
                state.form_filled = True


            '''
            required = [gender, gender_other, age, nationality, language, ethnicity, ethn_free, marital, marital_free, language, language_free, religion, religion_other, education, ses, home,  mum_education, dad_education, employment, self_emplo, mother_occ, father_occ, hobbies,  tech, know_nlp, use_nlp, would_nlp, use_ai]
            cond = [llm_use, usecases, contexts,  prompt1, prompt2, prompt3, prompt4, prompt5, prompt6, prompt7, prompt8, prompt9, prompt10]
            if None in required:
                st.warning("Please complete all required fields in the form.")
                st.warning(submitted)
            
            if use_ai == 'Never' and any(cond):
                st.warning('Only complete these sections if you have used AI chatbots.')
                st.warning(submitted)
            
            if use_ai == 'Every day' or use_ai ==  "Nearly every day" and None in [llm_use, usecases, contexts]:
                st.warning("Please fill in the sections about your use of AI")
                st.warning(submitted)
                submitted = False
            elif use_ai == 'Every day' or use_ai ==  "Nearly every day" and (not prompt1 or not prompt2 or not prompt3 or not prompt5 or not prompt5 or prompt1=="" or prompt2=="" or prompt3=="" or prompt4=="" or prompt5=="" ):
                st.warning("Please provide at least five prompts. You will receive a bonus for each additional answer. Responses will be manually checked.")
                st.warning(submitted)
                submitted = False
            else:
                demographic_information = [gender, gender_other, age, ';'.join(nationality), ';'.join(ethnicity), ethn_free,marital, marital_free, ';'.join(language),  language_free, religion, religion_other, education, mum_education, dad_education, ses, home, home_free, employment, ';'.join(self_emplo), ';'.join(mother_occ), ';'.join(father_occ), ';'.join(hobbies), hobbies_other]
                tech_information = [';'.join(tech), tech_other, ';'.join(know_nlp), know_other, ';'.join(use_nlp), use_nlp_other, ';'.join(would_nlp), would_other, use_ai, ';'.join(llm_use), llm_other, ';'.join(usecases), use_other, ';'.join(contexts), contexts_other]
                row = [annotator_id, session_id] + demographic_information + tech_information + [prompt1, prompt2, prompt3, prompt4, prompt5, prompt6, prompt7, prompt8, prompt9, prompt10, comments]
                write_to_file(row, url)
                placeholder.empty()
                state.form_filled = True
            '''


if state.form_filled:
    st.subheader("Thank you!")
    st.write("Thank you very much for completing the task. You can now return to Prolific and enter the code **{}**.".format('C116V1N5'))
