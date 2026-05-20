# Report — WAD LLM Chat

## Project overview

The project is a ChatGPT-like web application. Users can register, log in, create chat threads, send messages and receive LLM responses. Chat history is stored in PostgreSQL.

## Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy Async ORM
- Alembic
- Redis
- JWT
- GitHub OAuth
- HTML/CSS/JavaScript SPA-like frontend

## Asynchronous database interaction

Database interaction is implemented asynchronously using SQLAlchemy async tools:

- `create_async_engine`
- `async_sessionmaker`
- `AsyncSession`
- `async def get_db()`
- `await db.execute(...)`
- `await db.commit()`
- `await db.refresh(...)`

The application uses the async PostgreSQL driver:

```env
DATABASE_URL=postgresql+asyncpg://wad:wad@localhost:5432/wad
```

This fixes the synchronous database interaction issue.

## Architecture

The project uses an SPA-like UI and MCS backend structure:

- Models: `app/db/models.py`
- Controllers / routers: `app/auth/router.py`, `app/chats/router.py`
- Services: `app/auth/service.py`, `app/chats/service.py`, `app/llm/service.py`

## Database structure

### users

- id
- login
- hashed_password
- github_id
- created_at

### chats

- id
- title
- owner_id
- created_at

### messages

- id
- chat_id
- role
- content
- created_at

Relations:

- one user has many chats
- one chat has many messages

## API examples

### Register

`POST /api/auth/register`

Request:

```json
{"login":"anya","password":"123456"}
```

Response:

```json
{"access_token":"...","refresh_token":"...","token_type":"bearer"}
```

### Create chat

`POST /api/chats`

Header:

```text
Authorization: Bearer <access_token>
```

Request:

```json
{"title":"new chat"}
```

### Send message

`POST /api/chats/1/messages`

Request:

```json
{"content":"hello"}
```

Response contains both user message and assistant response.

## Screenshots and examples


1. ![login screen](screenshots/login.png)
2. ![chat screen](screenshots/chat.png)
3. ![messages screen](screenshots/messages.png)
4. ![docs screen](screenshots/docs.png)
5. ![example screen](screenshots/example.png)

## LLM service

The LLM logic is separated into `app/llm/service.py`. If `model.gguf` exists, the service can load a local GGUF model. If the model is missing, the app returns a mock response, which allows testing the full pipeline.
