from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import List
from service import service
from models import DndCombined

router = APIRouter(prefix="/external", tags=["External API"])


@router.get("/dnd/monster", response_model=DndCombined)
def get_dnd_monster() -> DndCombined:
    try:
        return service.get_random_monster()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dnd/monster/html", response_class=HTMLResponse)
def get_dnd_monster_html() -> str:
    try:
        monster = service.get_random_monster()

        image_html = ""
        if monster.image_url:
            image_html = f'<img src="{monster.image_url}" alt="{monster.name}" style="max-width:400px; margin:20px;" />'

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>D&D Monster - {monster.name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #1a1a1a;
                    color: #ffffff;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    text-align: center;
                    background-color: #2d2d2d;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.5);
                }}
                h1 {{
                    color: #ff6b6b;
                    margin-bottom: 20px;
                }}
                .stats {{
                    display: flex;
                    justify-content: space-around;
                    margin-top: 20px;
                    flex-wrap: wrap;
                }}
                .stat {{
                    background-color: #3d3d3d;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 5px;
                    min-width: 120px;
                }}
                .stat-label {{
                    color: #aaa;
                    font-size: 12px;
                    text-transform: uppercase;
                }}
                .stat-value {{
                    color: #4ecdc4;
                    font-size: 24px;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{monster.name}</h1>
                {image_html}
                <div class="stats">
                    <div class="stat">
                        <div class="stat-label">Type</div>
                        <div class="stat-value">{monster.type}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Challenge Rating</div>
                        <div class="stat-value">{monster.challenge_rating}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Hit Points</div>
                        <div class="stat-value">{monster.hit_points}</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        return html
    except Exception as e:
        return f"<h3>Error loading D&D monster info: {e}</h3>"


@router.get("/dnd/monsters/names", response_model=List[str])
def get_all_monster_names() -> List[str]:
    try:
        return service.get_all_monster_names()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))