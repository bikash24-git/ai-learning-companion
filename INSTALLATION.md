# Installation Guide - AI Learning Companion

## System Requirements
- Python 3.11 or higher
- 4GB RAM minimum
- Ollama installed and running

## Step-by-Step Installation

### 1. Install Ollama
- Download from: https://ollama.ai
- Follow installation instructions for your OS
- Start Ollama service

### 2. Download a Model
```bash
ollama pull qwen2
```

Other available models:
```bash
ollama pull mistral
ollama pull neural-chat
ollama pull llama2
```

### 3. Clone Repository
```bash
git clone https://github.com/bikash24-git/ai-learning-companion.git
cd ai-learning-companion
```

### 4. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env with your settings
```

### 7. Run Application
```bash
streamlit run app.py
```

Application will open at: http://localhost:8501

## Troubleshooting Installation

### Ollama Connection Error
- Ensure Ollama service is running
- Check if running on http://localhost:11434
- Verify model is downloaded

### Python Version Error
- Ensure Python 3.11+: `python --version`
- Use `python3` on macOS/Linux

### Permission Denied
- Run with sudo if needed
- Check folder permissions

### Module Not Found
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

## Verify Installation
```bash
# Check Python
python --version

# Check Ollama
curl http://localhost:11434/api/tags

# Test import
python -c "import streamlit; print('Streamlit OK')"
```

## Next Steps
After successful installation:
1. Upload a PDF or TXT file
2. Generate summaries
3. Create flashcards
4. Generate MCQs
5. Explore other features!
