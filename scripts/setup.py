#!/usr/bin/env python
"""
Setup script for the LLM chatbot project.
This script creates the necessary directory structure and configuration files.
"""
import os
import sys
import yaml
import subprocess
from pathlib import Path


def create_directory_structure():
    """Create the project directory structure."""
    directories = [
        "config",
        "src/llm",
        "src/memory",
        "src/retrieval",
        "src/interface",
        "src/utils",
        "data/raw",
        "data/processed",
        "data/conversations",
        "scripts",
        "tests"
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Create __init__.py files in Python package directories
        if directory.startswith("src") or directory.startswith("tests"):
            init_file = os.path.join(directory, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    pass
    
    print("Directory structure created successfully.")


def create_config_file():
    """Create the default configuration file."""
    config_path = "config/config.yml"
    
    # Default configuration
    config = {
        "model": {
            "name": "llama3:8b",
            "api": {
                "url": "http://localhost:11434/api/generate",
                "timeout": 60
            },
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 1000,
                "top_p": 0.9
            }
        }
    }
    
    print(f"Creating configuration file at {config_path}...")
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print("Configuration file created successfully.")


def check_ollama_installed():
    """Check if Ollama is installed and working correctly."""
    try:
        # Try running ollama version
        subprocess.run(["ollama", "--version"], check=True, capture_output=True)
        print("Ollama is installed.")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Ollama does not appear to be installed.")
        print("Please install Ollama from https://ollama.ai/")
        return False


def check_dependencies():
    """Check if required Python packages are installed."""
    try:
        import requests
        import yaml
        import dotenv
        
        print("Basic dependencies are installed.")
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required packages using:")
        print("pip install -r requirements.txt")
        return False


def run_setup():
    """Run the complete setup process."""
    print("Starting LLM Chatbot setup...")
    
    # Create directory structure
    create_directory_structure()
    
    # Create configuration file
    create_config_file()
    
    # Check dependencies
    dependencies_ok = check_dependencies()
    
    # Check Ollama installation
    ollama_ok = check_ollama_installed()
    
    # Summary
    print("\nSetup Summary:")
    print(f"- Directory structure: Created")
    print(f"- Configuration file: Created")
    print(f"- Dependencies: {'Installed' if dependencies_ok else 'Missing'}")
    print(f"- Ollama: {'Installed' if ollama_ok else 'Not found'}")
    
    # Next steps
    print("\nNext Steps:")
    if not dependencies_ok:
        print("1. Install Python dependencies: pip install -r requirements.txt")
    if not ollama_ok:
        print("2. Install Ollama from https://ollama.ai/")
        print("3. Pull the Mistral model: ollama pull mistral:7b")
    
    print("\nTo run the chatbot: python src/interface/cli.py")
    

if __name__ == "__main__":
    run_setup() 