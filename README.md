# WAD LLM Chat — async fixed version

This version fixes the teacher's comment: database interactions are asynchronous.

## Main fix

The project now uses:

- `create_async_engine`
- `async_sessionmaker`
- `AsyncSession`
- `async def` route handlers
- `await db.execute(...)`
- `await db.commit()`
- `await db.refresh(...)`

Application database URL:

```env
DATABASE_URL=postgresql+asyncpg://wad:wad@localhost:5432/wad
```

Alembic migrations still use a synchronous migration engine internally, so `alembic/env.py` converts the URL to `postgresql+psycopg2://...` only for migrations.

## Run on Windows PowerShell

```powershell
Copy-Item .env.example .env
docker compose up -d
python -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

Docs:

```text
http://localhost:8000/docs
```
