# 🗣️ Multilingual Voice Assistant using OpenRouter AI & Edge TTS

This is a Python-based multilingual voice assistant that:
- Listens to your voice commands
- Translates your speech to English
- Sends the query to a free OpenRouter AI model
- Translates the AI's answer into your chosen language
- Speaks the answer out loud using Microsoft's Edge TTS

## 🎯 Features

- 🔊 Speech recognition in multiple Indian & international languages
- 🌍 Google Translate integration for multilingual support
- 🧠 Uses powerful AI models via [OpenRouter API](https://openrouter.ai/)
- 🗣️ Realistic neural voices with Edge TTS (text-to-speech)
- 💾 Saves history of questions and answers
- 📌 CLI fallback when speech fails

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/mitanshhh/SpeakSmart.git
cd SpeakSmart
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```
---

## 📦 `requirements.txt`

```txt
SpeechRecognition
googletrans==4.0.0rc1
requests
edge-tts
playsound==1.2.2
pyttsx3
pyaudio
```


### 3. Get Your OpenRouter API Key
Sign up and get a free key from: https://openrouter.ai/

### 4. 🧪 Run the Assistant
```
python speaksmart.py
```
When prompted, speak your query or type it manually if the microphone doesn't capture clearly.

🌐 Supported Languages

| Language   | Code |
| ---------- | ---- |
| English    | en   |
| Hindi      | hi   |
| Marathi    | mr   |
| Tamil      | ta   |
| Telugu     | te   |
| Bengali    | bn   |
| Gujarati   | gu   |
| Urdu       | ur   |
| French     | fr   |
| German     | de   |
| Spanish    | es   |
| Portuguese | pt   |
| Russian    | ru   |

### 🧠 Models Used
By default, the assistant uses:

🧠 deepseek/deepseek-r1-0528:free via OpenRouter

You can change this in the search_info() function.

### 🔐 Privacy Note
No data is saved outside your local machine.

All history is stored in _history.txt_
