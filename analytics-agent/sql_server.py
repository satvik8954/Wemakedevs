import sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sql-analytics", stateless_http=True)

DB_PATH = "chinook.db"

@mcp.tool()
def run_sql(query: str) -> str:
    """Run a read-only SQL query against the Chinook music store database
    (tables: Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine,
    MediaType, Playlist, PlaylistTrack, Track) and return the results."""
    q = query.strip().lower()
    if not q.startswith("select"):
        return "Error: only SELECT queries are allowed."
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(query)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        conn.close()
        if not rows:
            return "Query ran successfully but returned no rows."
        result = ", ".join(cols) + "\n"
        result += "\n".join(", ".join(str(v) for v in row) for row in rows[:50])
        if len(rows) > 50:
            result += f"\n... ({len(rows) - 50} more rows truncated)"
        return result
    except Exception as e:
        return f"SQL error: {e}"

@mcp.tool()
def list_schema() -> str:
    """List all tables and their columns in the database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    out = []
    for t in tables:
        cur.execute(f"PRAGMA table_info({t})")
        cols = [row[1] for row in cur.fetchall()]
        out.append(f"{t}: {', '.join(cols)}")
    conn.close()
    return "\n".join(out)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
