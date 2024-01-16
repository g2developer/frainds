frainds
=============

PC voice recognition commander


## Features
- voice chat on chat AI like chatGPT, bard
- open and search webbrowser google(or bing, naver)
- open file browser

## Building from Source

- **Python:** Ensure that Python is installed on your system. You can download it from [python.org](https://www.python.org/).
- **Git:** Git is required for version control. If you don't have Git installed, you can download it from [git-scm.com](https://git-scm.com/).

Open a terminal and run the following commands.

1. **Set everything up.**

- Linux/Mac
```
git clone https://github.com/g2developer/frainds && cd frainds && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

- Windows (Command Prompt)
```
git clone https://github.com/g2developer/frainds && cd frainds && python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
```

2. **Build the app into an executable.**

```
pyinstaller main.spec
```

- The executable will be built in `frainds\dist\frainds`

3. **Alternatively you can instead run the app directly via Python.**

```
python main.py
```


&nbsp;
### Test environment
- python 3.8

### Used lib and model
- [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- [openai-whisper](https://github.com/openai/whisper)
- Pyqt6
- etc..

