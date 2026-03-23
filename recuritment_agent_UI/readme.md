# Recruitment Agent UI – Setup Guide

This project runs a **Recruitment Agent UI** built using Python, LangChain, and Streamlit.

Follow the steps below to set up the development environment and run the application.

---

## 1. Prerequisites

Make sure the following are installed on your system:

* Python 3.11
* Git
* Visual Studio Code

You can verify Python installation:

```
python --version
```

The recommended version for this project is **Python 3.11**.

---

## 2. Clone the Repository

```
git clone <repository-url>
cd recuritment_agent_UI
```

---

## 3. Create a Virtual Environment

Open the project folder in **VS Code** and open the integrated terminal.

Create a virtual environment:

```
python -m venv venv
```

---

## 4. Activate the Virtual Environment

### Windows (PowerShell)

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)

```
venv\Scripts\activate
```

### Linux / macOS

```
source venv/bin/activate
```

After activation you should see:

```
(venv)
```

in your terminal prompt.

---

## 5. Install Dependencies

Install the required Python libraries:

```
pip install google-generativeai
pip install langchain-google-genai
pip install langchain-community
pip install python-dotenv
pip install langchain-text-splitters
pip install langchain-classic
pip install langchain-core
pip install langchain
```

Install additional packages used for the UI and document processing:

```
pip install streamlit chromadb pypdf docx2txt
```

---

## 6. Verify Installation

Check that all packages are installed:

```
pip list
```

You should see packages such as:

* langchain
* streamlit
* chromadb
* google-generativeai

---

## 7. Run the Application

Start the Streamlit application using:

```
streamlit run app.py
```

After running the command, the application will open automatically in your browser.

Default local URL:

```
http://localhost:8501
```

---

## 8. Project Structure (Example)

```
recuritment_agent_UI
│
├── app.py
├── venv/
├── README.md
├── .env
└── requirements.txt
```

---

## 9. Deactivate Virtual Environment

When finished working:

```
deactivate
```

---

## 10. Notes

* Always activate the virtual environment before running the project.
* Install any additional dependencies inside the virtual environment only.
* Keep secrets such as API keys in the `.env` file.
