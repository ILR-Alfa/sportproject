from pydantic import BaseModel

class UserBase(BaseModel):
    telegram_id: int
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    badges: str
    stars: int

    class Config:
        orm_mode = True

class CompetitionBase(BaseModel):
    sport_type: str
    event_name: str

class CompetitionCreate(CompetitionBase):
    pass

class Competition(CompetitionBase):
    id: int
    is_finished: bool

    class Config:
        orm_mode = True

class PredictionBase(BaseModel):
    user_id: int
    competition_id: int
    predicted_result: str

class PredictionCreate(PredictionBase):
    pass

class Prediction(PredictionBase):
    id: int
    is_correct: bool

    class Config:
        orm_mode = True