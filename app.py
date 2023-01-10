import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import schemas
from chat import get_response
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    current_domain = request.url._url
    return templates.TemplateResponse("base.html", {"request": request, "domain": current_domain})


@app.get('/item/{id}', response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
@app.post("/predict")
async def predict(item: schemas.Item):
    response = get_response(item.message)
    message = {"answer": response}
    return message
# code for new branch
if __name__ == "__main__":
    uvicorn.run(app)
