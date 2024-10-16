import uvicorn
from fastapi import FastAPI
from databases import Sessionlocal, engine, Base
from routers import router 

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, workers=3)