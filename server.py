from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path(__file__).parent / "data.txt"


class TextPayload(BaseModel):
    text: str


@app.post("/api/data")
async def save_data(payload: TextPayload):
    """Принять текст и дописать его в data.txt."""
    with DATA_FILE.open("a", encoding="utf-8") as f:
        f.write(payload.text + "\n")
    return {"message": "Данные сохранены"}


@app.get("/api/data")
async def get_data():
    """Вернуть содержимое data.txt."""
    if not DATA_FILE.exists():
        return {"content": ""}
    content = DATA_FILE.read_text(encoding="utf-8")
    return {"content": content}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=3000, reload=True)