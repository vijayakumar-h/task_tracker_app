from contextlib import asynccontextmanager

import aiosqlite
from fastapi import FastAPI, Depends

from database import init_db, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/tasks')
async def read_tasks(db:aiosqlite.Connection = Depends(get_db)):
    async with db.execute("SELECT * FROM tasks") as cursor:
        rows = await  cursor.fetchall()
        return [dict(row) for row in rows]

@app.post('/tasks')
async def create_tasks(title: str, description: str, db: aiosqlite.Connection = Depends(get_db)):
    await  db.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (title, description)
    )
    await db.commit()
    return {"message": "Task created successfully"}

@app.patch('task/{task_id}')
async def toggle_task(task_id: int, completed: bool, db:aiosqlite.Connection = Depends(get_db)):
    await db.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    await db.commit()
    return {"message": "Task updated successfully"}

