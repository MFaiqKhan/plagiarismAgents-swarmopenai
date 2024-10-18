# Swarm-OpenAI Plagiarism Detection

![Project Logo](path/to/logo.png) <!-- Replace with your project's logo if available -->

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
  - [Swarm Package and Agents](#swarm-package-and-agents)
  - [Plagiarism Detection with Rabin-Karp](#plagiarism-detection-with-rabin-karp)
- [Advantages](#advantages)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

Swarm-OpenAI is an intelligent plagiarism detection system designed to analyze documents for potential plagiarized content efficiently and accurately. Leveraging the power of the **Swarm** package and advanced algorithms like **Rabin-Karp**, this project offers a robust solution for academic institutions, publishers, and content creators to ensure the originality of their work.

## Features

- **Automated Document Processing**: Upload and process documents seamlessly.
- **Section-Based Analysis**: Split documents into Introduction, Body, and Conclusion for targeted plagiarism checks.
- **Intelligent Agents**: Utilize specialized agents to analyze different sections of the document.
- **Efficient Plagiarism Detection**: Implement the Rabin-Karp algorithm with rolling hash functions for fast and accurate detection.
- **Comprehensive Reporting**: Generate detailed plagiarism reports highlighting matched instances.
- **Scalable Architecture**: Built to handle multiple documents concurrently with ease.

## Technologies Used

- **Python 3.8+**
- **Swarm**: A package for managing intelligent agents.
- **FastAPI**: For building the API endpoints.
- **Rabin-Karp Algorithm**: For efficient string matching in plagiarism detection.
- **Logging**: Comprehensive logging for monitoring and debugging.
- **HTTPX**: For handling HTTP requests.
- **OpenAI GPT-4**: For advanced language processing tasks.
- **dotenv**: For managing environment variables.

## How It Works

### Swarm Package and Agents

The **Swarm** package is the backbone of the Swarm-OpenAI project, enabling the orchestration of multiple intelligent agents to perform specialized tasks. Here's how it's integrated into the project:

1. **Agent Definition**: 
   - **Introduction Plagiarism Agent**: Analyzes the introduction section of a document.
   - **Body Plagiarism Agent**: Focuses on the main content or body.
   - **Conclusion Plagiarism Agent**: Examines the conclusion part.
   - **Triage Agent**: Determines which section to analyze and delegates tasks to the appropriate agents.

2. **Agent Communication**:
   - The **Triage Agent** receives the entire document and splits it into predefined sections.
   - Based on the content, it decides which specialized agent should analyze each section.
   - Each specialized agent uses the Rabin-Karp algorithm to detect plagiarism within its respective section.

3. **Advantages of Using Swarm and Agents**:
   - **Modularity**: Each agent handles a specific task, making the system easy to maintain and extend.
   - **Scalability**: New agents can be added without disrupting existing workflows.
   - **Parallel Processing**: Multiple agents can operate simultaneously, speeding up the analysis process.
   - **Flexibility**: Easily adaptable to different types of documents and analysis requirements.

### Plagiarism Detection with Rabin-Karp

The **Rabin-Karp** algorithm is employed to efficiently detect plagiarism by identifying matching n-grams between the target document and known source documents. Here's an overview of how it works:

1. **Preprocessing**:
   - The target document is split into words and then into overlapping n-grams (substrings of length `n`).
   - A rolling hash function computes a unique hash for each n-gram, allowing for quick comparisons.

2. **Hash Matching**:
   - Each hashed n-gram from the target document is compared against precomputed hashes from source documents.
   - If a hash match is found, the actual n-gram strings are compared to confirm plagiarism.

3. **Instance Recording**:
   - For each confirmed match, details such as the source document name, position in the target document, and the matched n-gram are recorded.
   - Once the number of matches exceeds a predefined threshold, it is flagged as plagiarism.

4. **Report Generation**:
   - Aggregated results from all sections are compiled into a comprehensive report, highlighting all detected instances of plagiarism.

#### Rolling Hash Function

A rolling hash function is integral to the efficiency of the Rabin-Karp algorithm. It allows the hash of an n-gram to be computed in constant time when moving through the text, rather than recalculating from scratch each time. This significantly reduces the computational overhead, especially for large documents.

## Advantages

- **High Accuracy**: The combination of intelligent agents and the Rabin-Karp algorithm ensures precise plagiarism detection.
- **Efficiency**: Optimized algorithms and parallel processing capabilities allow for rapid analysis, even for lengthy documents.
- **Detailed Reporting**: Generates comprehensive reports that provide clear insights into detected plagiarism instances.
- **Scalable and Modular**: Easily accommodates growing datasets and evolving analysis needs through its agent-based architecture.
- **User-Friendly**: Simplified upload and retrieval processes make it accessible for users with varying technical expertise.

## Installation

### Prerequisites

- **Python 3.8+**
- **Git**

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/swarm-openai.git
   cd swarm-openai
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```
     OPENAI_API_KEY=your_openai_api_key
     REPORTS_PATH=./backend/app/reports
     MAX_FILE_SIZE=1048576
     ALLOWED_CONTENT_TYPES=text/plain
     LOG_FILE=./backend/app/app.log
     ```

5. **Run Migrations or Setup (if applicable)**
   ```bash
   # Example if using a database
   python manage.py migrate
   ```

## Usage

### Running the Application

1. **Start the FastAPI Server**
   ```bash
   uvicorn backend.app.main:app --reload
   ```

2. **Upload a Document**
   - Use the provided script or API endpoint to upload a document for plagiarism analysis.
   ```bash
   python scripts/upload_and_process.py
   ```

3. **Retrieve the Report**
   - After processing, retrieve the plagiarism report using the document ID.
   ```bash
   python scripts/get_report.py
   ```

### API Endpoints

- **Check Processing Status**
  ```
  GET /status/{document_id}
  ```

- **Retrieve Plagiarism Report**
  ```
  GET /report/{document_id}
  ```

## Directory Structure
