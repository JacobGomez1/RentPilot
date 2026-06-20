from fastapi import APIRouter, HTTPException
import re

from app.data import apartments
from app.services import rank_apartments

router = APIRouter()


# -----------------------------
# GET ALL APARTMENTS
# -----------------------------
@router.get("/apartments")
def get_apartments():
    return apartments


# -----------------------------
# GET SINGLE APARTMENT
# -----------------------------
@router.get("/apartments/{apartment_id}")
def get_apartment(apartment_id: int):
    apartment = next(
        (a for a in apartments if a["id"] == apartment_id),
        None
    )

    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")

    return apartment


# -----------------------------
# QUERY PARSER (simple NLP-style filters)
# -----------------------------
def parse_query(query: str):
    query = query.lower()

    budget = None
    bedrooms = None
    pet_friendly = None
    city = None

    # Budget: "under 2000"
    match = re.search(r"(under|below|<)\s*\$?\s*(\d+)", query)
    if match:
        budget = int(match.group(2))

    # City
    if "austin" in query:
        city = "Austin"

    # Pet friendly
    if "pet" in query:
        pet_friendly = "Yes"

    # Bedrooms
    if "studio" in query:
        bedrooms = 0
    elif "1 bed" in query or "1 bedroom" in query:
        bedrooms = 1
    elif "2 bed" in query or "2 bedroom" in query:
        bedrooms = 2
    elif "3 bed" in query or "3 bedroom" in query:
        bedrooms = 3

    return {
        "budget": budget,
        "bedrooms": bedrooms,
        "pet_friendly": pet_friendly,
        "city": city,
    }


# -----------------------------
# SEARCH ENDPOINT
# -----------------------------
@router.get("/search")
def search_apartments(query: str = ""):
    filters = parse_query(query)

    results = apartments

    if filters["city"]:
        results = [a for a in results if a["city"] == filters["city"]]

    if filters["budget"] is not None:
        results = [a for a in results if a["price"] <= filters["budget"]]

    if filters["bedrooms"] is not None:
        results = [a for a in results if a["bedrooms"] == filters["bedrooms"]]

    if filters["pet_friendly"]:
        results = [a for a in results if a["pet_friendly"] == "Yes"]

    return rank_apartments(
        results,
        budget=filters["budget"],
        bedrooms=filters["bedrooms"],
        pet_friendly=filters["pet_friendly"]
    )