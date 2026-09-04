from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.connection import get_connection

router = APIRouter(prefix="/stores", tags=["stores"])


class Store(BaseModel):
    store_id: int
    name: str
    description: str
    location: str
    email: str
    phone: str
    status: str
    created_at: datetime
    updated_at: datetime


class StoreUpdate(BaseModel):
    name: str
    description: str
    location: str
    email: str
    phone: str
    status: str


class StorePatch(BaseModel):
    name: str | None = None
    description: str | None = None
    location: str | None = None
    email: str | None = None
    phone: str | None = None
    status: str | None = None


@router.get("/")
def read_root():
    return {"message": "E-commerce API is running!"}


@router.get("/stores")
def get_stores():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            store_id,
            name,
            description,
            location,
            email,
            phone,
            status,
            created_at,
            updated_at
        FROM stores
        """
    )

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    stores = []
    for row in rows:
        stores.append(
            {
                "store_id": row[0],
                "name": row[1],
                "description": row[2],
                "location": row[3],
                "email": row[4],
                "phone": row[5],
                "status": row[6],
                "created_at": row[7],
                "updated_at": row[8],
            }
        )

    return stores


@router.post("/stores")
def create_store(store: Store):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO stores
        (name, description, location, email, phone, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING
            store_id,
            name,
            description,
            location,
            email,
            phone,
            status,
            created_at,
            updated_at
        """,
        (
            store.name,
            store.description,
            store.location,
            store.email,
            store.phone,
            store.status,
        ),
    )

    row = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "store_id": row[0],
        "name": row[1],
        "description": row[2],
        "location": row[3],
        "email": row[4],
        "phone": row[5],
        "status": row[6],
        "created_at": row[7],
        "updated_at": row[8],
    }


@router.put("/stores/{store_id}")
def update_store(store_id: int, store: StoreUpdate):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE stores
        SET
            name = %s,
            description = %s,
            location = %s,
            email = %s,
            phone = %s,
            status = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE store_id = %s
        RETURNING
            store_id,
            name,
            description,
            location,
            email,
            phone,
            status,
            created_at,
            updated_at
        """,
        (
            store.name,
            store.description,
            store.location,
            store.email,
            store.phone,
            store.status,
            store_id,
        ),
    )

    row = cursor.fetchone()

    if row is None:
        connection.rollback()
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Store not found")

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "store_id": row[0],
        "name": row[1],
        "description": row[2],
        "location": row[3],
        "email": row[4],
        "phone": row[5],
        "status": row[6],
        "created_at": row[7],
        "updated_at": row[8],
    }


@router.patch("/stores/{store_id}")
def patch_store(store_id: int, store: StorePatch):
    connection = get_connection()
    cursor = connection.cursor()

    updates = []
    values = []

    if store.name is not None:
        updates.append("name = %s")
        values.append(store.name)

    if store.description is not None:
        updates.append("description = %s")
        values.append(store.description)

    if store.location is not None:
        updates.append("location = %s")
        values.append(store.location)

    if store.email is not None:
        updates.append("email = %s")
        values.append(store.email)

    if store.phone is not None:
        updates.append("phone = %s")
        values.append(store.phone)

    if store.status is not None:
        updates.append("status = %s")
        values.append(store.status)

    if not updates:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="No fields provided for update")

    updates.append("updated_at = CURRENT_TIMESTAMP")
    values.append(store_id)

    query = f"""
        UPDATE stores
        SET {', '.join(updates)}
        WHERE store_id = %s
        RETURNING
            store_id,
            name,
            description,
            location,
            email,
            phone,
            status,
            created_at,
            updated_at
    """
    cursor.execute(query, values)

    row = cursor.fetchone()

    if row is None:
        connection.rollback()
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Store not found")

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "store_id": row[0],
        "name": row[1],
        "description": row[2],
        "location": row[3],
        "email": row[4],
        "phone": row[5],
        "status": row[6],
        "created_at": row[7],
        "updated_at": row[8],
    }


@router.delete("/stores/{store_id}")
def delete_store(store_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM stores
        WHERE store_id = %s
        RETURNING store_id
        """,
        (store_id,),
    )

    row = cursor.fetchone()

    if row is None:
        connection.rollback()
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Store not found")

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message": "Store deleted successfully",
        "store_id": row[0],
    }
