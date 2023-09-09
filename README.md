# llmhandler : Simplify interacting with an LLM

## Goals
- [x] handle chatting with an llm
- [x] handle message history
- [x] allow easy addition of tools for llm function calling
- [ ] add thought prompting (automated continuous re-prompting done by the llm itself)
- [ ] handle config

## Usage
1. Prepare .env file with OPENAI_API_KEY
2. ``pip install -r requirements.txt``
3. See test.py for now..

## Modules

### Tools
- timezone_difference : Calculates the time difference for 2 given location

### llm.py
- Objects for message and message history
- Handles chatting with llm
  - automated function calling > function execution > llm response using function output