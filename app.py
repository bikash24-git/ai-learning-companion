"""
AI Learning Companion - Main Streamlit Application
A comprehensive tool for generating study materials from PDFs and TXT files using local LLM.
"""

import streamlit as st
import os
from pathlib import Path
from datetime import datetime

# Import services
from services.pdf_service import DocumentExtractor
from services.ollama_service import OllamaService
from database.schema import (
    initialize_database, add_file_record, get_file_records,
    add_summary, add_flashcard, add_mcq, add_important_question,
    get_summaries_by_file, get_flashcards_by_file, get_mcqs_by_file,
    get_important_questions_by_file, delete_file_and_data
)

# Configuration
UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

# Initialize session state
if 'ollama_service' not in st.session_state:
    st.session_state.ollama_service = OllamaService()

if 'connection_status' not in st.session_state:
    st.session_state.connection_status = None

if 'current_file' not in st.session_state:
    st.session_state.current_file = None

if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None


def check_ollama_connection():
    """Check and cache Ollama connection status."""
    if st.session_state.connection_status is None:
        with st.spinner("Checking Ollama connection..."):
            st.session_state.connection_status = st.session_state.ollama_service.check_connection()
    return st.session_state.connection_status


def display_header():
    """Display application header."""
    st.set_page_config(
        page_title="AI Learning Companion",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📚 AI Learning Companion")
        st.markdown("*Generate comprehensive study materials using AI*")
    
    with col2:
        if check_ollama_connection():
            st.success("✅ Ollama Connected")
        else:
            st.error("❌ Ollama Not Connected")


def display_sidebar():
    """Display sidebar navigation and settings."""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Ollama Model Selection
        st.subheader("Ollama Configuration")
        available_models = st.session_state.ollama_service.get_available_models()
        
        if available_models:
            selected_model = st.selectbox(
                "Select Model",
                available_models,
                index=0 if "qwen2" not in available_models else available_models.index("qwen2")
            )
            st.session_state.ollama_service.model = selected_model
        else:
            st.warning("No models found. Please ensure Ollama is running.")
            st.info("Download qwen2: `ollama pull qwen2`")
        
        # File Upload
        st.subheader("📤 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt'],
            help="Upload a PDF or TXT file"
        )
        
        if uploaded_file:
            file_type = uploaded_file.name.split('.')[-1].lower()
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Extract text
            try:
                with st.spinner(f"Extracting text from {file_type.upper()}..."):
                    extractor = DocumentExtractor()
                    extracted_text = extractor.extract_text(file_path, file_type)
                    file_size = extractor.get_file_size(file_path)
                    preview = extractor.get_text_preview(extracted_text)
                    
                    # Store in database
                    file_id = add_file_record(
                        uploaded_file.name,
                        file_type,
                        file_size,
                        preview
                    )
                    
                    st.session_state.current_file = {
                        'id': file_id,
                        'name': uploaded_file.name,
                        'type': file_type,
                        'text': extracted_text,
                        'size': file_size
                    }
                    st.session_state.extracted_text = extracted_text
                    
                    st.success("✅ Text extracted successfully!")
            
            except Exception as e:
                st.error(f"Error extracting text: {str(e)}")


def display_file_info():
    """Display current file information."""
    if st.session_state.current_file:
        with st.expander("📄 Current Document Info", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Name", st.session_state.current_file['name'][:30] + "...")
            with col2:
                st.metric("File Type", st.session_state.current_file['type'].upper())
            with col3:
                st.metric("Size", f"{st.session_state.current_file['size'] / 1024:.2f} KB")
            
            st.write("**Preview:**")
            st.text_area(
                "Extracted Content",
                st.session_state.extracted_text[:500] + "...",
                height=150,
                disabled=True
            )


def display_summary_generator():
    """Display summary generation interface."""
    st.subheader("📝 Summary Generator")
    
    if not st.session_state.current_file or not st.session_state.extracted_text:
        st.info("Please upload a document first.")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Generate Short Summary", key="short_summary"):
            with st.spinner("Generating short summary..."):
                try:
                    summary = st.session_state.ollama_service.generate_summary(
                        st.session_state.extracted_text,
                        "short"
                    )
                    add_summary(st.session_state.current_file['id'], 'short', summary)
                    st.success("✅ Summary Generated!")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        if st.button("Generate Detailed Summary", key="detailed_summary"):
            with st.spinner("Generating detailed summary..."):
                try:
                    summary = st.session_state.ollama_service.generate_summary(
                        st.session_state.extracted_text,
                        "detailed"
                    )
                    add_summary(st.session_state.current_file['id'], 'detailed', summary)
                    st.success("✅ Summary Generated!")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col3:
        if st.button("Generate Bullet Points", key="bullet_summary"):
            with st.spinner("Generating bullet point summary..."):
                try:
                    summary = st.session_state.ollama_service.generate_summary(
                        st.session_state.extracted_text,
                        "bullet"
                    )
                    add_summary(st.session_state.current_file['id'], 'bullet', summary)
                    st.success("✅ Summary Generated!")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error: {str(e)}")


def display_flashcard_generator():
    """Display flashcard generation interface."""
    st.subheader("🎴 Flashcard Generator")
    
    if not st.session_state.current_file or not st.session_state.extracted_text:
        st.info("Please upload a document first.")
        return
    
    num_cards = st.slider("Number of Flashcards", 5, 50, 10)
    
    if st.button("Generate Flashcards", key="gen_flashcards"):
        with st.spinner(f"Generating {num_cards} flashcards..."):
            try:
                flashcards = st.session_state.ollama_service.generate_flashcards(
                    st.session_state.extracted_text,
                    num_cards
                )
                
                for card in flashcards:
                    add_flashcard(
                        st.session_state.current_file['id'],
                        card['question'],
                        card['answer']
                    )
                
                st.success(f"✅ Generated {len(flashcards)} flashcards!")
                
                # Display flashcards
                for i, card in enumerate(flashcards, 1):
                    with st.expander(f"Flashcard {i}"):
                        st.write(f"**Q:** {card['question']}")
                        st.write(f"**A:** {card['answer']}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")


def display_mcq_generator():
    """Display MCQ generation interface."""
    st.subheader("❓ MCQ Generator")
    
    if not st.session_state.current_file or not st.session_state.extracted_text:
        st.info("Please upload a document first.")
        return
    
    num_questions = st.slider("Number of MCQs", 5, 50, 10)
    
    if st.button("Generate MCQs", key="gen_mcqs"):
        with st.spinner(f"Generating {num_questions} MCQs..."):
            try:
                mcqs = st.session_state.ollama_service.generate_mcqs(
                    st.session_state.extracted_text,
                    num_questions
                )
                
                for mcq in mcqs:
                    add_mcq(
                        st.session_state.current_file['id'],
                        mcq['question'],
                        mcq['option_a'],
                        mcq['option_b'],
                        mcq['option_c'],
                        mcq['option_d'],
                        mcq['correct_answer']
                    )
                
                st.success(f"✅ Generated {len(mcqs)} MCQs!")
                
                # Display MCQs
                for i, mcq in enumerate(mcqs, 1):
                    with st.expander(f"MCQ {i}: {mcq['question'][:50]}..."):
                        st.write(f"**A)** {mcq['option_a']}")
                        st.write(f"**B)** {mcq['option_b']}")
                        st.write(f"**C)** {mcq['option_c']}")
                        st.write(f"**D)** {mcq['option_d']}")
                        st.info(f"**Correct Answer: {mcq['correct_answer']}**")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")


def display_important_questions_generator():
    """Display important questions generation interface."""
    st.subheader("⭐ Important Questions Generator")
    
    if not st.session_state.current_file or not st.session_state.extracted_text:
        st.info("Please upload a document first.")
        return
    
    if st.button("Generate Important Questions", key="gen_imp_questions"):
        with st.spinner("Generating important questions..."):
            try:
                questions = st.session_state.ollama_service.generate_important_questions(
                    st.session_state.extracted_text
                )
                
                # Store in database
                for q in questions['short_answer']:
                    add_important_question(
                        st.session_state.current_file['id'],
                        q['question'],
                        'short_answer',
                        q['answer']
                    )
                
                for q in questions['long_answer']:
                    add_important_question(
                        st.session_state.current_file['id'],
                        q['question'],
                        'long_answer',
                        q['answer']
                    )
                
                for q in questions['exam_focused']:
                    add_important_question(
                        st.session_state.current_file['id'],
                        q['question'],
                        'exam_focused',
                        q['answer']
                    )
                
                st.success("✅ Important questions generated!")
                
                # Display questions by type
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Short Answer Questions**")
                    for i, q in enumerate(questions['short_answer'], 1):
                        with st.expander(f"Q{i}: {q['question'][:40]}..."):
                            st.write(q['answer'])
                
                with col2:
                    st.write("**Long Answer Questions**")
                    for i, q in enumerate(questions['long_answer'], 1):
                        with st.expander(f"Q{i}: {q['question'][:40]}..."):
                            st.write(q['answer'])
                
                with col3:
                    st.write("**Exam-Focused Questions**")
                    for i, q in enumerate(questions['exam_focused'], 1):
                        with st.expander(f"Q{i}: {q['question'][:40]}..."):
                            st.write(q['answer'])
            
            except Exception as e:
                st.error(f"Error: {str(e)}")


def display_study_materials():
    """Display previously generated study materials."""
    st.subheader("📚 Study Materials Repository")
    
    if not st.session_state.current_file:
        st.info("Upload a document to view study materials.")
        return
    
    file_id = st.session_state.current_file['id']
    
    tab1, tab2, tab3, tab4 = st.tabs(["Summaries", "Flashcards", "MCQs", "Important Questions"])
    
    with tab1:
        summaries = get_summaries_by_file(file_id)
        if summaries:
            for summary in summaries:
                with st.expander(f"📝 {summary['summary_type'].upper()} - {summary['generated_timestamp']}"):
                    st.write(summary['content'])
        else:
            st.info("No summaries generated yet.")
    
    with tab2:
        flashcards = get_flashcards_by_file(file_id)
        if flashcards:
            for i, card in enumerate(flashcards, 1):
                with st.expander(f"🎴 Card {i}: {card['question'][:50]}..."):
                    st.write(f"**Q:** {card['question']}")
                    st.write(f"**A:** {card['answer']}")
        else:
            st.info("No flashcards generated yet.")
    
    with tab3:
        mcqs = get_mcqs_by_file(file_id)
        if mcqs:
            for i, mcq in enumerate(mcqs, 1):
                with st.expander(f"❓ MCQ {i}: {mcq['question'][:50]}..."):
                    st.write(f"**{mcq['question']}**")
                    st.write(f"A) {mcq['option_a']}")
                    st.write(f"B) {mcq['option_b']}")
                    st.write(f"C) {mcq['option_c']}")
                    st.write(f"D) {mcq['option_d']}")
                    st.success(f"Correct: **{mcq['correct_answer']}**")
        else:
            st.info("No MCQs generated yet.")
    
    with tab4:
        questions = get_important_questions_by_file(file_id)
        if questions:
            short_q = [q for q in questions if q['question_type'] == 'short_answer']
            long_q = [q for q in questions if q['question_type'] == 'long_answer']
            exam_q = [q for q in questions if q['question_type'] == 'exam_focused']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Short Answer**")
                for q in short_q:
                    with st.expander(q['question'][:50]):
                        st.write(q['answer'])
            
            with col2:
                st.write("**Long Answer**")
                for q in long_q:
                    with st.expander(q['question'][:50]):
                        st.write(q['answer'])
            
            with col3:
                st.write("**Exam Focused**")
                for q in exam_q:
                    with st.expander(q['question'][:50]):
                        st.write(q['answer'])
        else:
            st.info("No important questions generated yet.")


def main():
    """Main application function."""
    # Initialize database
    initialize_database()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar()
    
    # Main content area
    if not check_ollama_connection():
        st.error("🔴 Cannot connect to Ollama. Please ensure:")
        st.markdown("""
        1. Ollama is installed: https://ollama.ai
        2. Ollama service is running
        3. A model is downloaded (e.g., `ollama pull qwen2`)
        4. Default address: http://localhost:11434
        """)
        return
    
    # Display current file info
    if st.session_state.current_file:
        display_file_info()
        
        # Create tabs for different features
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Summary",
            "Flashcards",
            "MCQs",
            "Important Questions",
            "Repository"
        ])
        
        with tab1:
            display_summary_generator()
        
        with tab2:
            display_flashcard_generator()
        
        with tab3:
            display_mcq_generator()
        
        with tab4:
            display_important_questions_generator()
        
        with tab5:
            display_study_materials()
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("👈 Upload a document from the sidebar to get started!")


if __name__ == "__main__":
    main()
