<div class="hero-icon" align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</div>
<h1 align="center"> AI Response Wrapper </h1> 
<h4 align="center">A lightweight Python backend that simplifies interaction with OpenAI's powerful language models for developers and users.</h4>
<h4 align="center">Developed with the software and tools below.</h4>
<div class="badges" align="center">
<img src="https://img.shields.io/badge/Framework-FastAPI-blue" alt="Framework: FastAPI">
<img src="https://img.shields.io/badge/Backend-Python-red" alt="Backend: Python">
<img src="https://img.shields.io/badge/Database-PostgreSQL-blue" alt="Database: PostgreSQL">
<img src="https://img.shields.io/badge/LLMs-OpenAI-black" alt="LLMs: OpenAI">
</div>
<div class="badges" align="center">
<img src="https://img.shields.io/github/last-commit/coslynx/AI-Response-Wrapper-MVP?style=flat-square&color=5D6D7E" alt="git-last-commit" />
<img src="https://img.shields.io/github/commit-activity/m/coslynx/AI-Response-Wrapper-MVP?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/languages/top/coslynx/AI-Response-Wrapper-MVP?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>  

## Overview

This repository contains the source code for the AI Response Wrapper, built as an MVP. This lightweight Python backend simplifies interaction with OpenAI's powerful language models for developers and users by reducing the complexity of API calls and response parsing, enabling efficient integration of AI-powered capabilities within applications and workflows. 

## Features

| Feature | Description |
|---|---|
| Request Handling | The wrapper receives user requests in the form of prompts and parameters, validates their syntax and format, and translates them into correctly structured API calls for OpenAI.  |
| API Communication | The wrapper securely communicates with OpenAI's API, sending validated requests and receiving responses. |
| Response Processing | The wrapper receives raw responses from the OpenAI API, performs error handling, and formats the responses into a usable format.  |
| Error Handling | The wrapper implements a robust error handling system to gracefully handle potential issues during API communication or response processing. |
| User Authentication | The wrapper implements a secure user authentication system using JWTs to control access to sensitive resources and manage user configurations. |
| Database Integration |  The wrapper stores user data and API logs securely in a PostgreSQL database for persistence, auditing, and analysis. |

## Architecture

The application follows a microservice architecture:

- **Backend:** Python server built with FastAPI handles requests and communication with OpenAI.
- **Database:** PostgreSQL database stores user information, API logs, and other relevant data.
- **OpenAI:**  OpenAI's powerful language models are accessed through their API.

## Dependencies

- Python 3.9+
- FastAPI
- Uvicorn
- SQLAlchemy
- Psycopg2-binary
- Pydantic
- OpenAI
- Requests
- JSON
- Argparse
- Logging
- PyJWT
- Python-dotenv

## Structure

```
└── app
    ├── main.py
    ├── routers
    │   ├── prompts
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   └── routes.py
    │   └── responses
    │       ├── __init__.py
    │       ├── models.py
    │       ├── routes.py
    │       └── services.py
    ├── database
    │   ├── __init__.py
    │   ├── models.py
    │   └── database.py
    └── utils
        ├── __init__.py
        ├── auth.py
        ├── error_handler.py
        ├── logger.py
        └── data_validation.py

```

## Installation

1. **Prerequisites:**
    - Python 3.9+
    - pip
    - PostgreSQL
    - OpenAI API key (sign up for an account and get your key from [https://platform.openai.com/](https://platform.openai.com/))
2. **Clone the repository:**
    ```bash
    git clone https://github.com/coslynx/AI-Response-Wrapper-MVP.git
    ```
3. **Navigate to the project directory:**
    ```bash
    cd AI-Response-Wrapper-MVP
    ```
4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5. **Set up environment variables:**
    - Create a `.env` file in the root directory.
    - Add the following environment variables:
        ```
        DATABASE_URL=postgresql://user:password@host:port/database_name
        OPENAI_API_KEY=your_openai_api_key
        SECRET_KEY=your_secret_key_here  
        ```
6. **Create the database:**
    ```bash
    python -m app.database.database create_all
    ```
7. **Start the application:**
    ```bash
    python -m app.main
    ```
    The application will be accessible at `http://localhost:8000`.

## Usage

1. **Access the API:** Send requests to the server using tools like `curl` or a programming language like Python.
2. **Authentication:**  Generate a JWT token using the `/auth/login` endpoint and include it in the `Authorization` header for subsequent requests.
3. **Send requests:** Use the `/prompts` and `/responses` endpoints for prompt handling and response generation. 

## Hosting

1. **Build the application:**  
    - (If necessary for your hosting provider)
2. **Choose a hosting provider:**
    - Consider platforms like Heroku, AWS, or other cloud providers.
3. **Configure your hosting provider:**
    - Follow the specific instructions for your chosen hosting provider.
    - Set up environment variables (including your database connection string and OpenAI API key).
4. **Deploy your application:**
    - Deploy the application to your chosen hosting provider.

## API Documentation

**Authentication:**
- The API requires an OpenAI API key and user authentication for security.
- Set up the `OPENAI_API_KEY` and `SECRET_KEY` environment variables before making API calls.
- Generate a JWT token using the `/auth/login` endpoint.
- Include the token in the `Authorization` header of all subsequent requests.

**Endpoints:**

- **`/auth/login`**
    - **Method:** POST
    - **Parameters:**
        - `username`:  (string)
        - `password`:  (string)
    - **Response:**
        - A JSON object containing the generated JWT token. 

- **`/prompts`**
    - **Method:** POST
    - **Parameters:**
        - `text`: (string) Prompt text.
        - `model`: (string) OpenAI model name.
        - `parameters`:  (optional, JSON) Model-specific parameters.
    - **Response:**
        - A JSON object containing the newly created prompt information.

- **`/responses`**
    - **Method:** POST
    - **Parameters:**
        - `prompt_id`:  (int) The ID of the prompt.
        - `model`: (string) OpenAI model name.
        - `parameters`: (optional, JSON) Model-specific parameters.
    - **Response:**
        - A JSON object containing the generated response. 


**Example API Call:**

```bash
curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'

```

```bash
curl -X POST http://localhost:8000/responses \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_jwt_token" \
     -d '{"prompt_id": 1, "model": "text-davinci-003", "parameters": {"temperature": 0.7}}'
```

**Example API Response:**

```json
{
  "id": 1,
  "text": "This is a test prompt.",
  "model": "text-davinci-003",
  "parameters": "{}",
  "user_id": 1,
  "responses": []
}
```

```json
{
  "id": 1,
  "text": "This is the response to the test prompt.",
  "model": "text-davinci-003",
  "parameters": "{\"temperature\": 0.7}",
  "generation_time": "2024-03-28T12:34:56.789Z",
  "prompt_id": 1
}
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any suggestions, bug fixes, or improvements.

## License

This project is licensed under the MIT License.

### 🤖 AI-Generated MVP
This MVP was entirely generated using artificial intelligence through [CosLynx.com](https://coslynx.com).
          
          No human was directly involved in the coding process of the repository: AI-Response-Wrapper-MVP
        
          ### 📞 Contact
          For any questions or concerns regarding this AI-generated MVP, please contact CosLynx at:
          - Website: [CosLynx.com](https://coslynx.com)
          - Twitter: [@CosLynxAI](https://x.com/CosLynxAI)

          <p align="center">
            <h1 align="center">🌐 CosLynx.com</h1>
          </p>
          <p align="center">
            <em>Create Your Custom MVP in Minutes With CosLynxAI!</em>
          </p>
          <div class="badges" align="center">
          <img src="https://img.shields.io/badge/Developers-Drix10,_Kais_Radwan-red" alt="">
          <img src="https://img.shields.io/badge/Website-CosLynx.com-blue" alt="">
          <img src="https://img.shields.io/badge/Backed_by-Google,_Microsoft_&_Amazon_for_Startups-red" alt="">
          <img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4,_v6-black" alt="">
          </div>