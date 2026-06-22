# AI Learning Companion 📚

An intelligent, AI-powered productivity tool designed to help students learn effectively by automatically generating comprehensive study materials from PDFs and text files using a local LLM (Large Language Model).

## 🌟 Features

### Core Capabilities
- **📤 Document Upload**: Support for PDF and TXT files
- **🔍 Text Extraction**: Intelligent extraction from various document formats
- **📝 Summary Generator**: Create summaries in multiple formats
- **🎴 Flashcard Generator**: Auto-generate study flashcards
- **❓ MCQ Generator**: Create multiple-choice questions with answers
- **⭐ Important Questions**: Generate exam-focused questions
- **💾 SQLite Database**: Persistent storage of all generated materials

### AI Features
1. **Summary Types**
   - Short Summary (2-3 sentences)
   - Detailed Summary (5-7 sentences)
   - Bullet Point Summary (5-10 key points)

2. **Flashcard Generation**
   - Customizable number of cards
   - Question-Answer format
   - Easy to review and export

3. **MCQ Generation**
   - 10 questions per generation
   - 4 options each (A, B, C, D)
   - Clear answer marking
   - Exam-ready format

4. **Important Questions**
   - Short Answer Questions
   - Long Answer Questions
   - Exam-Focused Questions

### User Interface
- Professional Streamlit dashboard
- Sidebar navigation
- File upload area
- Results display section
- Loading indicators
- Error messages
- Responsive layout

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Ollama installed and running locally
- A downloaded LLM model (e.g., qwen2)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-learning-companion.git
cd ai-learning-companion
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Ollama**
```bash
# Download Ollama from https://ollama.ai
# Start Ollama service
ollama pull qwen2  # Download a model
```

5. **Run the application**
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
ai-learning-companion/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── README.md             # This file
├── development_log.md    # Development history
│
├── database/
│   ├── schema.py         # SQLite schema and database functions
│   └── learning_companion.db  # SQLite database (auto-created)
│
├── uploads/              # Uploaded files directory (auto-created)
│
├── services/
│   ├── __init__.py       # Services module initialization
│   ├── pdf_service.py    # PDF extraction service
│   └── ollama_service.py # Ollama LLM integration
│
├── templates/            # UI templates (reserved)
├── screenshots/          # Application screenshots (reserved)
└── assets/              # Static assets (reserved)
```

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit 1.28.1 |
| LLM | Ollama + qwen2 |
| Database | SQLite3 |
| PDF Processing | PyPDF2 4.0.1 |
| HTTP Client | Requests 2.31.0 |
| Data Validation | Pydantic 2.5.0 |
| Language | Python 3.11+ |

## 📊 Database Schema

### Files Table
Stores metadata about uploaded documents
```sql
- id (PRIMARY KEY)
- filename (UNIQUE)
- file_type
- upload_timestamp
- file_size
- content_preview
```

### Summaries Table
```sql
- id (PRIMARY KEY)
- file_id (FOREIGN KEY)
- summary_type (short, detailed, bullet)
- content
- generated_timestamp
```

### Flashcards Table
```sql
- id (PRIMARY KEY)
- file_id (FOREIGN KEY)
- question
- answer
- generated_timestamp
```

### MCQs Table
```sql
- id (PRIMARY KEY)
- file_id (FOREIGN KEY)
- question
- option_a, option_b, option_c, option_d
- correct_answer
- generated_timestamp
```

### Important Questions Table
```sql
- id (PRIMARY KEY)
- file_id (FOREIGN KEY)
- question
- question_type (short_answer, long_answer, exam_focused)
- answer
- generated_timestamp
```

## 🎯 Usage Guide

### Step 1: Upload Document
- Click "Choose a file" in the sidebar
- Select a PDF or TXT file
- File is automatically processed

### Step 2: Generate Study Materials
- Navigate to desired feature tab
- Adjust parameters (number of items)
- Click generate button
- Wait for AI to process

### Step 3: Review and Study
- View results immediately
- Access "Repository" tab for previously generated materials
- Export or print as needed

### Step 4: Organize Learning
- All materials are automatically saved
- Revisit anytime in the Repository
- Build comprehensive study notes

## ⚙️ Configuration

### Ollama Settings
Edit in sidebar:
- **Model Selection**: Choose from available models
- **Temperature**: Adjust AI creativity (0.0-1.0)
- **Connection**: Auto-detected

### File Settings
- Maximum file size: Dependent on system RAM
- Supported formats: PDF, TXT
- Upload directory: `./uploads/`

## 📝 API Reference

### DocumentExtractor
```python
from services.pdf_service import DocumentExtractor

extractor = DocumentExtractor()
text = extractor.extract_text("file.pdf", "pdf")
preview = extractor.get_text_preview(text, max_length=500)
```

### OllamaService
```python
from services.ollama_service import OllamaService

ollama = OllamaService(base_url="http://localhost:11434", model="qwen2")

# Check connection
if ollama.check_connection():
    # Generate summary
    summary = ollama.generate_summary(text, "short")
    
    # Generate flashcards
    flashcards = ollama.generate_flashcards(text, num_cards=10)
    
    # Generate MCQs
    mcqs = ollama.generate_mcqs(text, num_questions=10)
    
    # Generate important questions
    questions = ollama.generate_important_questions(text)
```

### Database Functions
```python
from database.schema import (
    initialize_database,
    add_file_record,
    add_summary,
    get_summaries_by_file,
    # ... other functions
)

initialize_database()
file_id = add_file_record("document.pdf", "pdf", 5000, preview_text)
add_summary(file_id, "short", summary_content)
```

## 🔧 Troubleshooting

### Issue: "Ollama Not Connected"
**Solution:**
1. Ensure Ollama is installed: https://ollama.ai
2. Start Ollama service
3. Check if running on http://localhost:11434
4. Download a model: `ollama pull qwen2`

### Issue: "No models found"
**Solution:**
```bash
ollama pull qwen2
# or
ollama pull mistral
ollama pull neural-chat
```

### Issue: Text extraction fails
**Solution:**
- Ensure PDF is not encrypted
- Verify file format is correct
- Check file is not corrupted
- Try with a different PDF

### Issue: Slow generation
**Solution:**
- Reduce text length
- Use a faster model
- Check system resources
- Increase timeout

## 📈 Performance Tips

1. **Optimize Text Length**: Shorter documents generate faster
2. **Choose Efficient Models**: `qwen2` is recommended
3. **System Resources**: Allocate sufficient RAM
4. **Batch Operations**: Generate multiple items together
5. **Database Maintenance**: Regular cleanup of old records

## 🔒 Security Features

- Local-only LLM processing
- No data sent to external servers
- SQLite encryption-ready
- File validation before processing
- Error handling for malformed inputs

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional file format support (DOCX, PPT)
- Export features (PDF, Excel)
- Advanced search in study materials
- Collaborative features
- Mobile app support

## 📄 License

This project is open source and available under the MIT License.

## 🙋 Support

For issues and questions:
1. Check troubleshooting section
2. Review GitHub issues
3. Create new issue with details
4. Include error messages and logs

## 🚀 Roadmap

- [ ] DOCX and PPTX support
- [ ] PDF export of study materials
- [ ] Study progress tracking
- [ ] Spaced repetition algorithm
- [ ] Mobile-friendly version
- [ ] Offline mode
- [ ] Multi-language support
- [ ] Cloud backup option

## 📚 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## 🎓 Created for

AI Vibe Coding Challenge - Building innovative AI-powered learning tools for students worldwide.

---

**Made with ❤️ for better learning** | Version 1.0.0
