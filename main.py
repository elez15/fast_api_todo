from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import TodoCreate, TodoResponse
from database import session_local, custom_base, engine
from models import TodoModel

# main step to create a table based on our need
custom_base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency for DB session
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"Message": "FastAPI working !!!!!!!!!!!"}


# post - created with path /todos
@app.post("/todos", response_model=TodoResponse)
# input we will be converted as dict using model dump method
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoModel(**todo.model_dump())
    # adding data into databse
    db.add(db_todo)
    # make sure data is saved using commit
    db.commit()
    # refresh to reload the things
    db.refresh(db_todo)

    return db_todo


# To get al the todo in list
@app.get("/todos", response_model=list[TodoResponse])
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()


# todo_id is path parameter, which will be expected in the function
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_single_todo(todo_id: int, db: Session = Depends(get_db)):
    # we filtering by id and also the first occurance
    res_id = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not res_id:
        raise HTTPException(status_code=404, detail="Todo ID not found.")
    return res_id


# to update single todos
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_single_todo(
    todo_id: int, update_data: TodoCreate, db: Session = Depends(get_db)
):
    res_id = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not res_id:
        raise HTTPException(status_code=404, detail="Todo ID not found.")
    for key, value in update_data.model_dump().items():
        setattr(res_id, key, value)
    db.commit()
    db.refresh(res_id)
    return res_id


# to delete the entery
# here we are not sending any response back so we will ignore response model
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    res_id = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not res_id:
        raise HTTPException(status_code=404, detail="Todo ID not")
    db.delete(res_id)
    db.commit()
    return {"message": f"Todo-{todo_id} deleted successfully."}
