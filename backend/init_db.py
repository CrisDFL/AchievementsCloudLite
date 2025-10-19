from sqlalchemy import create_engine
from models import Base
engine = create_engine('sqlite:///achievements.db')
Base.metadata.create_all(engine)
print("DB initialized")
