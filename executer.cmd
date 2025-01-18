python segmenter.py
set /p Key=<key.txt
setx OPENAI_API_KEY %Key%
python simplifier.py