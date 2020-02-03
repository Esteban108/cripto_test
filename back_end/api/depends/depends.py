from back_end.api.data_access import SessionLocal


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

