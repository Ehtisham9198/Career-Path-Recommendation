import os
import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain



api_version = os.getenv("OPENAI_API_VERSION")
api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")


llm = AzureChatOpenAI(
    deployment_name="TourMitr",
    api_key=api_key,
    api_version=api_version
)
template = """
Based on the user's information, recommend 5 career paths to the user with 10 words desciption, best on top:
Interests: {user_interests}
Hobbies: {user_hobbies}
Skills: {user_skills}
Education: {user_education}
Work Experience: {user_experience}
Career Goals: {user_goals}
Preferred Work Environment: {user_preferences}
Values: {user_values}
"""


prompt_template = PromptTemplate.from_template(template)


llm_chain = LLMChain(prompt=prompt_template, llm=llm)

# Streamlit
st.set_page_config(page_title="Career Path Recommendation", page_icon=":briefcase:", layout="wide")


st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        text-align: center;
        font-size: 16px;
        border-radius: 10px;
        border: none;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Career Path Recommendation")
st.markdown("""
Welcome to the Career Path Recommendation tool! Please provide the following information to receive personalized career path recommendations.
""")


with st.container():
    st.header("User Information")

    user_interests = st.multiselect(
        "Interests",
        options=["Technology", "Artificial Intelligence", "Solving Complex Problems", "Design", "Marketing", "Finance", "Other"]
    )
    if "Other" in user_interests:
        other_interests = st.text_input("Please specify other interests")
        user_interests.append(other_interests)

    user_hobbies = st.multiselect(
        "Hobbies",
        options=["Reading", "Hiking", "Playing Chess", "Painting", "Gardening", "Cooking", "Other"]
    )
    if "Other" in user_hobbies:
        other_hobbies = st.text_input("Please specify other hobbies")
        user_hobbies.append(other_hobbies)

    user_skills = st.multiselect(
        "Skills",
        options=["Programming", "Data Analysis", "Problem-Solving", "Communication", "Project Management", "Design", "Other"]
    )
    if "Other" in user_skills:
        other_skills = st.text_input("Please specify other skills")
        user_skills.append(other_skills)

    user_education = st.selectbox(
        "Education",
        options=["High School", "Associate's Degree", "Bachelor's Degree", "Master's Degree", "PhD", "Other"]
    )
    if user_education == "Other":
        user_education = st.text_input("Please specify other education")

    user_experience = st.selectbox(
        "Work Experience",
        options=["None", "Internship", "1-2 years", "3-5 years", "5+ years", "Other"]
    )
    if user_experience == "Other":
        user_experience = st.text_input("Please specify other work experience")

    user_goals = st.text_input("Career Goals", "To become a data scientist or machine learning engineer")

    user_preferences = st.selectbox(
        "Preferred Work Environment",
        options=["Remote", "In-Office", "Hybrid", "Flexible", "Other"]
    )
    if user_preferences == "Other":
        user_preferences = st.text_input("Please specify other preferred work environment")

    user_values = st.multiselect(
        "Values",
        options=["Work-Life Balance", "Continuous Learning", "Innovation", "Team Collaboration", "Leadership", "Creativity", "Other"]
    )
    if "Other" in user_values:
        other_values = st.text_input("Please specify other values")
        user_values.append(other_values)

if st.button("Get Career Recommendations"):
    with st.spinner("Generating recommendations..."):
        inputs = {
            "user_interests": ", ".join(user_interests),
            "user_hobbies": ", ".join(user_hobbies),
            "user_skills": ", ".join(user_skills),
            "user_education": user_education,
            "user_experience": user_experience,
            "user_goals": user_goals,
            "user_preferences": user_preferences,
            "user_values": ", ".join(user_values)
        }


        response = llm_chain.run(inputs)
        st.success("Career Path Recommendations:")
        st.write(response)
