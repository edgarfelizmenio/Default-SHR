from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = automap_base()
engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/raw_shr')
Base.prepare(engine, reflect=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                autoflush=False,
                                bind=engine))

Base.query = db_session.query_property()

import models