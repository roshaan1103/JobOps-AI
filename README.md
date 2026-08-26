# JobOps AI

JobOps AI is a local-first AI-powered job search and application automation platform.

The system is designed to:

- discover relevant jobs
- collect jobs from multiple permitted sources
- normalize and deduplicate jobs
- analyze job requirements
- match jobs against a candidate profile
- rank opportunities
- explain job matches
- customize resumes using verified candidate evidence
- generate application documents
- track applications
- automate workflows
- maintain human approval before application submission

## Architecture

JobOps AI uses a hybrid architecture combining:

- FastAPI
- PostgreSQL
- Streamlit
- Ollama
- Local LLMs
- Embeddings
- RAG
- FAISS
- n8n
- Docker
- GitHub Actions

## Current Status

Phase 1 — Engineering Foundation

Current components:

- FastAPI backend
- Streamlit frontend
- PostgreSQL
- n8n
- Docker Compose
- Basic health checks
- Automated backend tests

## Development Philosophy

JobOps AI is designed around:

1. Local-first development
2. Free/open-source technologies where practical
3. Deterministic logic where AI is unnecessary
4. AI for contextual reasoning and generation
5. Human-in-the-loop application approval
6. Modular job-source connectors
7. Security from the beginning
8. Incremental engineering

## Project Status

This project is under active development.