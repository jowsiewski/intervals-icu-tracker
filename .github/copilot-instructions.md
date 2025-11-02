# Intervals.icu Activity Tracker - Project Instructions

This is a Python FastAPI project for fetching and managing activities from intervals.icu API.

## Project Structure
- FastAPI backend with REST endpoints
- SQLAlchemy for database operations
- Pydantic models for data validation
- httpx client for intervals.icu API integration
- APScheduler for automated data fetching

## Development Guidelines
- Use Python type hints throughout the codebase
- Follow FastAPI best practices for API design
- Implement proper error handling for external API calls
- Use environment variables for sensitive configuration
- Write comprehensive tests for API endpoints

## API Integration
- Store intervals.icu API credentials securely
- Implement rate limiting for external API calls
- Cache frequently accessed data
- Handle API errors gracefully

## Database
- Use SQLAlchemy models for all entities
- Implement proper relationships between models
- Use Alembic for database migrations
- Follow database best practices for indexing