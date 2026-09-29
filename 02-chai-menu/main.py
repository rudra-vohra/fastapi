from fastapi import FastAPI,Query,HTTPException
from data import menu_items
from models import MenuItems,MenuResponse

app = FastAPI(
    title="Chai Point menu API",
    description=(
        "Read only menu API for Chai Point"
    )
)

@app.get(
        '/',
        summary="Health Check",
        description=(
            "Health check route for startup"
        )
    )
def root():
    return {
        "message":"Server is up and running smoothly"
    }


@app.get(
        '/menu',
        summary="Menu Items",
        description=(
            "Returns the menu items present."
        ),
        response_model=MenuResponse,
        tags=["menu"]
    )
def get_menu(category: str | None = Query(None,description="filter by chai, snacks or combo")):
    if category:
        filtered = [item for item in menu_items if item['category'] == category.lower()]
        if not filtered:
            raise HTTPException(status_code=404,detail=f"No item found of category: {category}")
        return MenuResponse(count= len(filtered),items=filtered)

    return MenuResponse(count=len(menu_items),items=filtered)


@app.get(
        '/menu/{item_id}',
        summary="Menu Item by Id",
        description=(
            "Returns the menu item by id."
        ),
        response_model=MenuItems,
        tags=["menu"]
    )
def get_item(item_id: int):
    for item in menu_items:
        if item['id'] == item_id:
            return item

    raise HTTPException(status_code=404,detail=f"No item found of ID: {item_id}")