from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Path
from database import database, engine, metadata
from models import budget, anvelopes
from schemas import CreateBudget, Budget, CreateAnvelope
import sqlalchemy

@asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# Allow requests from your Vue app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.post("/api/budget/create")
async def create_budget(budget_req:CreateBudget):
    print(budget_req)
    query = budget.insert().values(dict(budget_req))
    book_id = await database.execute(query)
    print(book_id)

@app.get("/api/budget/load")
async def get_budget():
    query = budget.select()
    result = await database.fetch_all(query)
    result_as_dicts = [dict(row) for row in result]
    return result_as_dicts

@app.delete("/api/budget/delete/{budget_id}")
async def delete_budget(budget_id: int):
    # First delete all envelopes associated with this budget
    # This prevents foreign key constraint violations
    envelopes_query = anvelopes.delete().where(anvelopes.c.budget_id == budget_id)
    await database.execute(envelopes_query)

    # Then delete the budget itself
    budget_query = budget.delete().where(budget.c.id == budget_id)
    result = await database.execute(budget_query)

    return {"message": f"Budget {budget_id} and all its envelopes deleted successfully"}

@app.get("/api/anvelopes/load/{budget_id}")
async def get_anvelopes(budget_id: int):
    query = anvelopes.select().where(anvelopes.c.budget_id == budget_id)
    result = await database.fetch_all(query)
    result_as_dicts = [dict(row) for row in result]
    return result_as_dicts

@app.post("/api/anvelopes/create")
async def create_anvelopes(anvelope_req:CreateAnvelope):
    query = anvelopes.insert().values(dict(anvelope_req))
    result = await database.execute(query)
    print(result)
    return result

@app.post("/api/anvelopes/add_money/{envelope_id}/{amount}")
async def add_money(envelope_id: int, amount: int):
    query = anvelopes.update().where(anvelopes.c.id == envelope_id).values(anvelope_budget=anvelopes.c.anvelope_budget + amount)
    result = await database.execute(query)
    return result

@app.post("/api/anvelopes/spend_money/{envelope_id}/{amount}")
async def spend_money(envelope_id: int, amount: int):
    query = anvelopes.update().where(anvelopes.c.id == envelope_id).values(anvelope_budget=anvelopes.c.anvelope_budget - amount)
    result = await database.execute(query)
    return result

@app.delete("/api/anvelopes/delete/{envelope_id}")
async def delete_envelope(envelope_id: int):
    query = anvelopes.delete().where(anvelopes.c.id == envelope_id)
    result = await database.execute(query)
    return result
