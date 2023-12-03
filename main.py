import pandas as pd
from fastapi import UploadFile, Depends, Request, File
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from config import app, get_db
from models import Users
from fastapi.responses import RedirectResponse
import starlette.status as status


templates = Jinja2Templates(directory="templates")
@app.get("/")
def import_user_from_csv(request: Request, db: Session = Depends(get_db)):
    data = db.query(Users).all()
    print(data)
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.post("/result")
async def read_item(file: UploadFile = UploadFile(...), db: Session = Depends(get_db),):
    try:
        contents = await file.read()
        binary_to_str = contents.decode('ascii')
        splitted_data = binary_to_str.split("\r\n")
        if splitted_data:
            for info in splitted_data:
                if info not in ['', 'name,age', 'Name,Age']:
                    print(info)
                    user_data = info.split(',')
                    print(user_data, "---")
                    user_model = Users(name=str(user_data[0]), age=int(user_data[1]))
                    db.add(user_model)
                    db.commit()
                else:
                    pass
            return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        else:
            return {"message": "Something went wrong"}
    except Exception as e:
        return {"message": str(e)}
