# Local testing commands

From the root of the Space folder:

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python scripts/check_input_files.py
python app.py
```

Then open the local Gradio URL shown in your terminal, usually:

```text
http://127.0.0.1:7860
```
