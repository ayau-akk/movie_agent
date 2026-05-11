# ‘Film Buff’ AI Agent

## Project Description

The ‘Film Buff’ AI Agent is a local agent built on Ollama and LangChain that answers questions about films.

The agent uses the OMDb API to retrieve information about films. It can search for films, display ratings, retrieve plot summaries, compare films and remember the context of the conversation.

## Selected option

Option 2: Local model + LangChain.

Option weighting: 1.1

## Stack

- Python 3.11.4
- LangChain
- langchain-ollama
- Ollama
- qwen2.5:7b
- OMDb API
- ConversationBufferMemory
- requests
- python-dotenv

## Agent capabilities

The agent can:

1. Search for a film by title
2. Search for a list of films by keyword
3. Retrieve the full film synopsis
4. Retrieve the film’s rating
5. Remember the user’s name
6. Remember the user’s preferences
7. Call upon multiple tools for complex queries
8. Display reasoning via LangChain’s verbose mode

## Implemented tools

The project implements 4 tools:

1. search_movie_by_title — search for a film by title
2. search_movies_list — search for a list of films
3. get_full_movie_plot — retrieve the full plot
4. get_movie_rating — retrieve the IMDB rating

## Memory

The project uses ConversationBufferMemory.

The memory allows the agent to remember:

- the user’s name
- favourite films
- favourite genres
- favourite directors
- the context of previous messages

Example:

User: My name is Asel  
Agent: I’ll remember that your name is Asel.

User: What’s my name?  
Agent: Your name is

Translated with DeepL.com (free version)
