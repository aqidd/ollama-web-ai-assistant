# Web AI assistant using local LLM

## Overview

This repo can be used to build your own AI assistant with Ollama. 
The improvements made from original repo are:
- Adding super simple web crawler to get links from your base URL 
- Replace Open AI with Ollama. [How to run Ollama](https://ollama.ai/blog/ollama-is-now-available-as-an-official-docker-image)

Notes:
- Change base URL/initial page in data_pipeline.py before processing
- If you get timeout while processing query, increase ServiceContext request_timeout
- To change model, replace Ollama model parameter. This repo is using mistral

See the original README below for your references.

---

# Building a Blog AI assistant using Retrieval Augmented Generation

## Overview

In this guide, we will build an LLM Chatbot that uses Retrieval Augmented Generation to answer questions about a particular blog or a list of blogs. We use LlamaIndex to chunck the blog text and build index, and then provide this context from the blog chunks along with the prompt to the GPT-4 model to build the chatbot.

By the end of this session, you will have an interactive web application deployed that helps answer questions from the blog.

## Step-By-Step Guide

For prerequisites, environment setup, step-by-step guide and instructions, please refer to the [QuickStart Guide](https://quickstarts.snowflake.com/guide/build_rag_based_blog_ai_assistant_using_streamlit_openai_and_llamaindex/index.html?index=..%2F..index#0).
