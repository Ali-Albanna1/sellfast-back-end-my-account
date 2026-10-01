# database.py

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
from config.environment import db_URI

# Connect FastAPI with SQLAlchemy
engine = create_engine(
    db_URI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def migrate_service_price_range():
    """Add and backfill service price-range columns for existing databases."""
    with engine.begin() as connection:
        inspector = inspect(connection)
        if "services" not in inspector.get_table_names():
            return

        columns = {column["name"] for column in inspector.get_columns("services")}

        if "price_min" not in columns:
            connection.execute(text("ALTER TABLE services ADD COLUMN price_min FLOAT"))
        if "price_max" not in columns:
            connection.execute(text("ALTER TABLE services ADD COLUMN price_max FLOAT"))

        if "price" in columns:
            connection.execute(text("""
                UPDATE services
                SET price_min = COALESCE(price_min, CASE name
                        WHEN 'Laptop Repair' THEN 100.00
                        WHEN 'Mobile Screen Replacement' THEN 60.00
                        WHEN 'Software Installation' THEN 30.00
                        WHEN 'Data Recovery' THEN 150.00
                        WHEN 'Home Network Setup' THEN 90.00
                        ELSE price
                    END),
                    price_max = COALESCE(price_max, CASE name
                        WHEN 'Laptop Repair' THEN 150.00
                        WHEN 'Mobile Screen Replacement' THEN 80.00
                        WHEN 'Software Installation' THEN 50.00
                        WHEN 'Data Recovery' THEN 200.00
                        WHEN 'Home Network Setup' THEN 120.00
                        ELSE price
                    END)
            """))

            missing_ranges = connection.execute(text("""
                SELECT COUNT(*)
                FROM services
                WHERE price_min IS NULL OR price_max IS NULL
            """)).scalar_one()
            if missing_ranges:
                raise RuntimeError("Cannot remove legacy service prices before all ranges are populated")

            connection.execute(text("ALTER TABLE services DROP COLUMN price"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
