from pydantic import BaseModel


class TodoBase(BaseModel):
    # to validate our field inputs, when we send through API post request
    title: str
    description: str | None = None
    completed: bool = False


class TodoCreate(TodoBase):
    """
    Docstring for TodoCreate

    Inherited from Todobase
    """

    pass


class TodoResponse(TodoBase):
    """
    Docstring for TodoResponse
    To send response back to user or any
    so we added ID
    """

    id: int

    class Config:
        # we get data input from ORM model only
        # As a response this mode will converts to JSON if it is an ORM data
        orm_mode = True
