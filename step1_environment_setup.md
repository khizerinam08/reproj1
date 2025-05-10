# Step 1: Environment Setup

## 1. Create Conda Environment

First, let's set up a conda environment with Python 3.12:

```bash
# Create a new conda environment
conda create -n llm-chatbot python=3.12

# Activate the environment
conda activate llm-chatbot
```

## 2. Create Project Directory Structure

Now, let's create the project directory structure:

```bash
# Create main project directory
mkdir -p llm-chatbot
cd llm-chatbot

# Create subdirectories
mkdir -p config src/llm src/memory src/retrieval src/interface src/utils data/raw data/processed scripts tests
```

## 3. Initialize Python Packages

Create the necessary `__init__.py` files to make the directories Python packages:

```bash
# Create __init__.py files
touch src/__init__.py
touch src/llm/__init__.py
touch src/memory/__init__.py
touch src/retrieval/__init__.py
touch src/interface/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

## 4. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai/):

For Windows:
- Download the installer from the website
- Run the installer and follow the instructions

For Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

For macOS:
- Download the macOS application from the website
- Move it to your Applications folder

## 5. Pull the Mistral 7B Model

After installing Ollama, pull the Mistral 7B model:

```bash
ollama pull mistral:7b
```

## 6. Create requirements.txt

Create a basic requirements.txt file with initial dependencies:

```bash
# Create requirements.txt
cat > requirements.txt << EOL
requests==2.31.0
python-dotenv==1.0.0
langchain==0.1.9
langchain-community==0.0.19
EOL
```

## 7. Install Dependencies

Install the dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

## 8. Create Configuration File

Create a basic configuration file:

```bash
# Create config directory and file
mkdir -p config
cat > config/config.yml << EOL
model:
  name: mistral:7b
  api:
    url: http://localhost:11434/api/generate
    timeout: 60
  parameters:
    temperature: 0.7
    max_tokens: 1000
    top_p: 0.9
EOL
```

## 9. Verify Setup

Test that Ollama is working correctly:

```bash
ollama run mistral:7b "Hello, are you working correctly?"
```

Now you have set up the environment and basic project structure for your LLM chatbot. In the next step, we'll implement the basic Ollama client. 