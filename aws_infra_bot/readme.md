# AWS Infra Chatbot POC

An Agentic AI assistant built with **LangChain** and **Streamlit** to monitor AWS resource compliance.

## Features
* **Compliance Checks:** Leverages AWS Config to find non-compliant resources.
* **Tagging Audit:** Identifies resources missing mandatory enterprise tags.
* **Public Access Audit:** Flags S3 buckets with open ACLs.

## Setup
1. **Clone & Install:**
   ```bash
   pip install streamlit langchain langchain-aws boto3 python-dotenv