import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm


DATABASE_URL = "postgresql://docker-pom_oltp_db_ct:sjukebarna123@localhost/pathofmodifiers_db"

engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()