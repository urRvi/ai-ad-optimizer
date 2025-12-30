from sqlmodel import SQLModel, Field, create_engine, Session
engine = create_engine("sqlite:///adoptimizer.db", echo=False)

def init():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
