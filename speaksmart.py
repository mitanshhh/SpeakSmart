import speech_recognition as sr
from googletrans import Translator
import requests
import uuid, os, asyncio
from playsound import playsound
import edge_tts
import json
import pyttsx3

API_KEY = "" #Enter your API KEY here 
if not API_KEY:
    API_KEY = str(input("Enter openrouter API key: "))


engine = pyttsx3.init()
engine.setProperty('rate', 185)     
engine.setProperty('volume', 1.0)   
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  


translator = Translator()
recognizer = sr.Recognizer()

voice_map = {
    "hi": "hi-IN-SwaraNeural",      # Hindi
    "mr": "mr-IN-AarohiNeural",     # Marathi
    "ta": "ta-IN-PallaviNeural",    # Tamil
    "te": "te-IN-MohanNeural",      # Telugu
    "bn": "bn-BD-NabanitaNeural",   # Bengali
    "gu": "gu-IN-DhwaniNeural",     # Gujarati
    "ur": "ur-PK-AsadNeural",       # Urdu
    "en": "en-US-JennyNeural",      # English
    "fr": "fr-FR-DeniseNeural",     # French
    "de": "de-DE-KatjaNeural",      # German
    "it": "it-IT-ElsaNeural",       # Italian
    "es": "es-ES-ElviraNeural",     # Spanish
    "pt": "pt-PT-FernandaNeural",   # Portuguese
    "ru": "ru-RU-SvetlanaNeural"    # Russian
}


print("""
| Language  | Code |    | Language  | Code |
| --------  | ---- |    | --------  | ---- |
| English   |  en  |    | Bengali   |  bn  |
| Hindi     |  hi  |    | Tamil     |  ta  |
| Marathi   |  mr  |    | Telgu     |  te  |
| German    |  de  |    | Gujrati   |  gu  |
| French    |  fr  |    | Portuguese|  pt  |
| Spanish   |  es  |    | Russian   |  ru  |
""")

valid_lang_codes = ["en", "hi", "mr", "de", "fr", "es", "bn", "ta", "te", "gu", "pt", "ru"]

engine.say("Kindly specify your source language and the language in which you would like the response")
engine.runAndWait()

#Get language input from user
try:
    src_language = input("The command would be in (e.g., 'hi' for Hindi): ").strip().lower()

    if src_language not in valid_lang_codes:
        src_language = "en"

    dest_language = input("Answer would be in which language (e.g., 'en' for English): ").strip().lower()
    if dest_language not in valid_lang_codes:
        dest_language = "en"
except KeyboardInterrupt:
    print("⛔ Interrupted")
    exit()

text_input = ""

#Function to post request to openrouter API
def search_info(query):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": [{"role": "user", "content": query}]
        })
    )
    if response.status_code == 200:
        print("\033[F\033[K", end='')
        print("🔍 Search found!")
        try:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except (KeyError, TypeError, json.JSONDecodeError):
            return None
    else:
        print(f"API Error: {response.status_code}, {response.text}")
        return None
    

#Function to save data as history
def save_info(question, answer):
    with open("history.txt", "a", encoding="utf-8") as file:
        file.write(f"\nUSER: {question} ({src_language})\n")
        file.write(f"ANSWER:\n {answer} \n\n")


#Function to speak through edgeTTS
async def speak(text, voice, rate=1.1):
    filename = f"{uuid.uuid4().hex}.mp3"

    rate_percent = f"{int((rate - 1) * 100)}%"
    if not rate_percent.startswith('-'):
        rate_percent = '+' + rate_percent

    try:
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate_percent)
        await communicate.save(filename)
        playsound(filename)
    finally:
        if os.path.exists(filename):
            os.remove(filename)


with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)

while True:
    try:
        with sr.Microphone() as source:
            print("🎧 Listening...")
            audio = recognizer.listen(source)
            print("🧠 Recognizing...")
            text_input = recognizer.recognize_google(audio, language=src_language) 
            print(f"🗣️  User said: {text_input}\n")
            print("Searching...")
            
            if any(word in text_input.lower() for word in ["quit", "exit"]): #Exit options
                print("Thank you for using.")
                exit()

    #Set input question default to user through keyboard 
    except sr.UnknownValueError:
        print("Sorry, I could not understand.\n")
        text_input = str(input("Search: "))
        if not text_input:
            print("Invalid Search, restart again")
            exit()

        #Exit options
        print("\nSearching...")
        if any(word in text_input.lower() for word in ["quit", "exit"]):
            print("Thank you for using.")
            exit()

        #Request Error through API
    except sr.RequestError:
        print("Could not connect to Google Speech Recognition.")
        continue

        #Any other Exceptions
    except Exception as e:
        print(f"An error occurred: {e}")
        continue

        #Keyboard interrupt 
    except KeyboardInterrupt:
        print("Thank you for using.")
        exit()

    #step 1: Translate query to english 
    translated_query_eng = translator.translate(text=text_input, src=src_language, dest="en").text

    try:
        #Step 2:Search for that answer in English
        query_answer_english = search_info(translated_query_eng)
        if not query_answer_english:
            print("No answer received from API.") #Check if answer exists
            continue

        #Step 3: Translate answer back to the user language
        translated_answer = translator.translate(query_answer_english, src="en", dest=dest_language)

        #Remove unwanted symbols from answer
        prettify_answer = translated_answer.text.replace("**", "").replace("<think>","").replace("###","").strip()
        
        #Handle exception
    except Exception as searcherror:
        print("❌ Error during AI search or translation:", searcherror)
        continue

    if prettify_answer:
        print("🔊 Converting information into audio\n")
        try:
            voice = voice_map.get(dest_language, "en-US-JennyNeural")
            asyncio.run(speak(prettify_answer, voice, rate=1.1)) #Change rate as per user demand (1 is normal)

            #For Keyboard Interrupt save answer in history.txt
            #Exit once saved
        except KeyboardInterrupt:
            print("⛔ Interrupted")
            save_info(translated_query_eng, prettify_answer)
            print("Information saved successfully ✅")
            exit()
        except Exception as e:
            print("Audio playback error:", e)

    try:
        #Save data in history.txt at end of audio
        save_info(translated_query_eng, prettify_answer)
        print("Information saved successfully ✅\n")
    except Exception as file_save_error:
        print("❌ Error updating history:", file_save_error)
    except KeyboardInterrupt:
        exit()

    #Ask if user wants to ask anything more 
    restart_code = input(("Got something more to ask? (Y/n): ")) #Default is set to YES
    if any(word in restart_code.lower() for word in ["n","quit", "exit","no","nope"]):
        print("Thankyou for using.")
        exit()
    else:
        continue
    
