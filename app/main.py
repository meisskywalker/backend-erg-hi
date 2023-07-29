from dotenv import load_dotenv
import uvicorn

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from db import engine
from routers import product

app = FastAPI()

origins = ["http://localhost:5173", "https://erg-hi.netlify.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

# app.include_router(auth.router)
app.include_router(product.router)
# app.include_router(image.router)
# app.include_router(user.router)
# app.include_router(hero.router)
# app.include_router(about_us.router)
# app.include_router(contact_us.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
