import speech_recognition as sr

def speechProcess():

    # Initialize recognizer class                                       
    r = sr.Recognizer()
    # audio object                                                         
    audio = sr.AudioFile("test1.wav")
    #read audio object and transcribe
    with audio as source:
        audio = r.record(source)                  
        result = r.recognize_google(audio)
    
    print(result)

speechProcess()