# Learnice

## Overview
This project is a web application consisting of:

Vue Frontend: A Vue.js-based frontend that serves the user interface.
FastAPI Backend: A Python FastAPI backend for handling the application's API.
LLM Scripts: A set of scripts for fine-tuning a language model.
To run the project, both the frontend and backend must be running simultaneously.

## Requirements
Node.js: Version v16.15.0
Python: Version 3.9.18 with pip installed
Dependencies: Installed via npm for the frontend and pip for the backend

## Backend setup
1. create a python virtual environment (optional but recommended)
- python3 -m venv venv
- source venv/bin/active 
2. install project dependancies
- cd learnice-backend
- **IMPORTANT**: replace '<path_to_project>' in line 50 of requirements.txt with the path to your project
- pip3 install -r requirements.txt
3. start the backend project
- uvicorn main:app --reload

The backend includes a .env file pre-configured with necessary credentials for running an AWS service.
This file has been included to simplify setup and avoid requiring you to create and configure an AWS account.
No changes are needed to this file.

## Frontend setup
1. Navigate to project directory
cd learnice-frontend
2. install project dependancies
npm install
3. start the development server
npm run dev

## LLM scripts
The llm/ folder contains scripts for fine-tuning a language model (mbert-base-multilingual-cased). These scripts are standalone and do not require the frontend or backend to be running. To use these scripts:

Ensure Python is installed with the necessary libraries (requirements.txt).
Run the scripts directly from the llm/ folder.

## Usage
Start the backend with uvicorn main:app --reload.
Start the frontend with npm run dev.
Open the application in your browser at http://localhost:5173.

## llm files
llms/:
- finetune_mbert.py: The script where the fine-tuned model is trained on preprocessed dataset.
- test_tuned_model.py: A script used to test and observed the predicted tags of the fine-tuned model on different sentences
- evaluate_fine_tuned.py: script used to evaluate performance of the fine tuned model
- MIM_GOLD_DESCRIPTION_EN_tagset.pdf: reference for the meaning of each tag within the MIM-Gold dataset

llms/lang-classification:
- evaluate_lang_classifier.py: script used to evaluate the performance of the language classifier model
- lang_classifier.py: script to train the language classifier used to classify a sentence as Icelandic or English
