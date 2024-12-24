from fastapi import FastAPI

from db.db_setup import engine
from db.models import user, task
from authroutes.auth import router as auth_router
from taskroutes.task import router as task_router

user.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="FAST API TODO",
description="ToDo List Application.",
contact={
    "name": "M.Waqas",
    "email": "abdullahwaqas22@gmail.com"

},
license_info={
    "name": "Associate Software Engineer"
}
)


app.include_router(auth_router)
app.include_router(task_router)