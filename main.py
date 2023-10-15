import streamlit as st
import openai
from src.config import API_KEY
import speech_synthesis
import speech_ingest
import azure.cognitiveservices.speech as speechsdk

# Set the title and favicon for your website
st.set_page_config(
    page_title="DubCare",
    page_icon="🏥"
)

# Navigation Bar
st.sidebar.title("How DubCare Works:")
page = st.sidebar.selectbox("\n", ["Home Page", "Speech to Text", "Live Interaction", "Text to Speech"])

# Define the content for each page
if page == "Home Page":
    st.title("DubCare")
    st.write("DubCare is a healthcare oriented technology which seeks to improve and strengthen connections between healthcare organizations and their users through the assistance of AI.")
    st.image("https://sapphireventures.com/wp-content/uploads/2023/02/Sapphire-Blog-Hero_Paving-the-Future-of-Digital-Healthcare.jpg")
    st.write("DubCare aims to benefit not only caretakers and hospital staff, but also the patients and questions they interact with. We want to make sure that the role of doctor and nurses"+  
             " aren't replaced, but aided by the addition of artificial intelligence being able to streamline their workflows. By improving connection and automating the process of making" +
             " appointments and saving not only the patient's time, but the nurses' who are then freed up to work on other tasks, we can much better benefit the hospital system in their services to" +
             " the people." +
             " Built as a hackathon project by Aryan Damle, Lwazi Mabota, and Ares Zhang. Utilizes StreamLit as a lightweight frontend while using Microsoft Azure Cognitive Services and OpenAI APIS as" + 
             " backend functionalities.")
    

elif page == "Speech to Text":
    st.title("Speech to Text")
    st.write("A smart voicemail inbox. The AI parses the speech message, converting it to a string for use by the AI.")
    audio_file = open('test1.wav','rb') #enter the filename with filepath

    audio_bytes = audio_file.read() #reading the file

    st.audio(audio_bytes, format='audio/ogg') #displaying the audio
    

elif page == "Live Interaction":
    st.title("💬 DubCare Live AI Help System ")
    listening = False 
    speech_config = speechsdk.SpeechConfig(subscription="c3b9f8dc287749e4a3ef23c4c3d46e33", region="westus2")
    speech_config.speech_recognition_language = "en-US"
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    with st.sidebar:
        openai_api_key = API_KEY

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "What can I help PATIENT_NAME with today?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
    
    if st.button("Start Microphone"):
        st.write("Listening... Speak into your microphone.")
    
        speech_recognition_failed = False  # Flag to track if recognition failed
        listening = True 
        
    if (st.button("End Microphone")): listening = False 
    
    openai.api_key = openai_api_key
    try:
        while listening:
            result = speech_recognizer.recognize_once_async().get()
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                user_input = result.text
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.chat_message("user").write(user_input)
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
                msg = response.choices[0].message
                st.session_state.messages.append(msg)
                st.chat_message("assistant").write(msg.content)
            elif result.reason == speechsdk.ResultReason.NoMatch and not speech_recognition_failed:
                st.write("No speech could be recognized.")
                speech_recognition_failed = True  # Set the flag to True to indicate failure
            elif result.reason == speechsdk.ResultReason.NoMatch and speech_recognition_failed:
                pass  # If recognition fails again, do nothing
    except KeyboardInterrupt:
        pass
    finally:
         st.write("Microphone input stopped.")
         
        
elif page == "Text to Speech":
    st.title("🗣️ DubCare Text-to-Speech")
    st.write("This is where DubCare will utilize Microsoft Azure Text -> Speech Systems to convert the text into suitable Speech for the user.")
    if st.button('Speech'):
        speech_synthesis.speechSynth()
        st.write("Hello User, I've got all your current information on file and your appointment with Dr. Miller is booked for Saturday at 12:00pm. We will see you then!")