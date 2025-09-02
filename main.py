# main.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict

# Pydantic 모델 정의
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

# 메모리 내 데이터 저장소
fake_items_db: Dict[int, Item] = {}

# --- API 엔드포인트 정의 ---

# 루트 경로
@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Simple Item API!"}

# 아이템 생성 (Create)
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    new_item_id = max(fake_items_db.keys()) + 1 if fake_items_db else 1
    fake_items_db[new_item_id] = item
    # ID를 포함하여 반환 (간단하게 딕셔너리로)
    return {"item_id": new_item_id, **item.dict()}

# 모든 아이템 조회 (Read All)
@app.get("/items/", response_model=list) # 응답 모델을 리스트로 명시
async def read_all_items(skip: int = 0, limit: int = 10):
    all_items = [
        {"item_id": item_id, **item.dict()}
        for item_id, item in fake_items_db.items()
    ]
    return all_items[skip : skip + limit]

# 특정 아이템 조회 (Read One)
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return fake_items_db[item_id]

# 아이템 수정 (Update)
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    fake_items_db[item_id] = item
    return item

# 아이템 삭제 (Delete)
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del fake_items_db[item_id]
    return # No Content 응답
