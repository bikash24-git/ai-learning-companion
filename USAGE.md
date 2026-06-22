# Usage Guide - AI Learning Companion

## Starting the Application

```bash
streamlit run app.py
```

Application opens at: http://localhost:8501

## User Interface Overview

### Sidebar
- **Ollama Configuration**: Select model and check connection
- **File Upload**: Upload PDF or TXT files
- **Settings**: Adjust application settings

### Main Content Area
- **Tabs**: Different features (Summary, Flashcards, MCQs, Questions, Repository)
- **File Info**: Current document details
- **Results Display**: Generated study materials

## Feature Usage

### 1. Summary Generation

**Short Summary** (2-3 sentences)
- Quick overview of document
- Best for: Quick reference

**Detailed Summary** (5-7 sentences)
- Comprehensive overview
- Best for: Deep learning

**Bullet Points** (5-10 points)
- Key points listed
- Best for: Quick review

**Steps:**
1. Upload document
2. Go to "Summary" tab
3. Click desired summary type
4. Wait for generation
5. View or export results

### 2. Flashcard Generation

**Parameters:**
- Number of cards: 5-50 (default: 10)

**Steps:**
1. Upload document
2. Go to "Flashcards" tab
3. Adjust slider for number of cards
4. Click "Generate Flashcards"
5. Review generated cards
6. Use "Repository" to revisit

**Tips:**
- More cards = longer generation time
- 10-15 cards are optimal
- Cards are sorted by importance

### 3. MCQ Generation

**Features:**
- 4 options per question (A, B, C, D)
- Clear correct answers
- Exam-ready format

**Steps:**
1. Upload document
2. Go to "MCQs" tab
3. Adjust slider for number of questions
4. Click "Generate MCQs"
5. Review questions and answers
6. Use for practice tests

**Tips:**
- 10 questions recommended
- Review correct answers
- Use for self-assessment

### 4. Important Questions

**Question Types:**
- **Short Answer**: 2-4 word answers
- **Long Answer**: Paragraph answers
- **Exam Focused**: Key exam questions

**Steps:**
1. Upload document
2. Go to "Important Questions" tab
3. Click "Generate Important Questions"
4. View questions by type
5. Study each category

**Tips:**
- Focus on exam-focused questions first
- Use for exam preparation
- Mix with other study methods

### 5. Study Repository

**Access:**
- Go to "Repository" tab
- View all generated materials
- Organized by type (Summaries, Flashcards, MCQs, Questions)

**Features:**
- Expandable sections
- Timestamps for tracking
- Easy review

**Tips:**
- Revisit materials often
- Compare different summary types
- Use for comprehensive studying

## Best Practices

### For Effective Learning
1. **Start with Summaries**: Get document overview
2. **Create Flashcards**: Test knowledge
3. **Practice MCQs**: Exam preparation
4. **Review Questions**: Deep understanding
5. **Revisit Repository**: Reinforcement learning

### Document Tips
- Use well-formatted PDFs
- Ensure text is readable (not scanned images)
- Organize by chapters or topics
- Upload one document at a time

### Generation Tips
- Start with smaller numbers (5-10)
- Wait for generation to complete
- Review quality before exporting
- Regenerate if unsatisfied

### Study Tips
- Study flashcards daily
- Practice MCQs multiple times
- Write answers to long questions
- Mix study methods
- Take breaks every 25 minutes

## Keyboard Shortcuts
- `R`: Refresh page
- `S`: Toggle sidebar
- `Ctrl+C`: Stop generation

## Troubleshooting Usage

### Generation is Slow
- Check system resources
- Reduce document size
- Use faster model
- Close other applications

### Poor Quality Results
- Verify document quality
- Try different document
- Adjust model temperature
- Regenerate with different settings

### File Won't Upload
- Check file format (PDF/TXT only)
- Verify file is not corrupted
- Check file size
- Try different file

## Advanced Tips

### Model Selection
- **qwen2**: Recommended, balanced
- **mistral**: Faster, good quality
- **neural-chat**: Specialized for conversation

### Temperature Adjustment
- **Lower (0.3-0.5)**: More consistent
- **Higher (0.7-0.9)**: More creative
- **Default (0.7)**: Balanced

### Batch Processing
- Upload multiple documents
- Generate all materials
- Compare results
- Study using repository

## Export Options (Future)
- PDF export
- Excel export
- Print optimization
- Cloud backup
