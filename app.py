import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType

st.set_page_config(
    page_title="Elearning Course Creator",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Elearning Course Creator")
st.sidebar.markdown("## Welcome to the Elearning Course Creator!")
st.sidebar.markdown(
    "This App Harnesses power of Lyzr Automata to generate Elearning Courses. You Need to specify your Topic and Target Audience and This app will Craft Elearning Course for your topic")

api = st.sidebar.text_input("Enter our OPENAI API KEY Here", type="password")

if api:
    openai_model = OpenAIModel(
        api_key=api,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )
else:
    st.sidebar.error("Please Enter Your OPENAI API KEY")


def course_creator(topics, audiences):
    course_agent = Agent(
        prompt_persona="You Are Expert Elearning Course Creator",
        role="Course creator",
    )

    course_task = Task(
        name="Course Creation Task",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=course_agent,
        log_output=True,
        instructions=f"""You are an Expert Elearning Course creator.Your task is to create course based on used given input topic and specific Audience.

        Input Requirements:
        Specific Topic: User Enters topic for which they want to create course
        Specific Audience: user specifies for which audience they are making this course
        
        Output Requirements:
        Course Title: Course title is SEO friendly and Eye Catchy for specific audience
        Learning Objectives: Specify Learning objectives from generated course.Make objectives point wise and give bullet points for sub sections.
        Course Structure: Specify Course Structure With Module and in each module specify lessons
        Assessment Strategies: Specify Assessment strategies
        Anticipated Impact: Specify Anticipated Impact by doing this course
        
        Below is User Input:
        Topic : {topics}
        Audience: {audiences}
        """,
    )

    output = LinearSyncPipeline(
        name="Generate Course",
        completion_message="Course Generated!",
        tasks=[
            course_task
        ],
    ).run()
    return output[0]['task_output']


topic = st.text_input("Specify Topic", placeholder="Digital Marketing Fundamentals")
audience = st.text_input("Specify Audience", placeholder="Small business owners and entrepreneurs")

if api and st.button("Generate"):
    solution = course_creator(topic, audience)
    st.markdown(solution)

