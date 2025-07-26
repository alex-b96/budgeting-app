from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from database import metadata

budget = Table(
    "budget",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("total_budget", Integer),
)

anvelopes = Table(
    "anvelopes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("anvelope_name", Integer),
    Column("anvelope_budget", Integer),
    Column("budget_id", ForeignKey("budget.id"))
)
