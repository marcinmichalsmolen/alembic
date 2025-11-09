# Ćwiczenia praktyczne 1-4 SQLAlchemy
# Autor: Marcin Smoleń

from datetime import datetime, timezone
from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    Table,
    Column,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    declarative_base,
    relationship,
    DeclarativeBase,
    Session
)


# ===============================================================
# 1. Inicjalizacja bazy danych
# ===============================================================

engine = create_engine("sqlite:///eksperymenty.db", echo=True)


# ===============================================================
# 2. Klasa bazowa
# ===============================================================

class Base(DeclarativeBase):
    pass


# ===============================================================
# 3. Modele z relacją 1-wiele
# ===============================================================

class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    type: Mapped[int] = mapped_column(Integer)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)

    # relacja 1-wiele (Experiment -> DataPoints)
    datapoints: Mapped[list["DataPoint"]] = relationship(
        back_populates="experiment",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Experiment(id={self.id}, title='{self.title}', finished={self.finished})>"


class DataPoint(Base):
    __tablename__ = "datapoints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float)
    target_value: Mapped[float] = mapped_column(Float)

    # klucz obcy wskazujący na tabelę experiments
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"))

    # odwrotna strona relacji (wiele-do-jeden)
    experiment: Mapped["Experiment"] = relationship(back_populates="datapoints")

    def __repr__(self):
        return (
            f"<DataPoint(id={self.id}, real_value={self.real_value}, "
            f"target_value={self.target_value}, experiment_id={self.experiment_id})>"
        )


# ===============================================================
# 4. Tworzenie bazy danych i tabel
# ===============================================================

Base.metadata.create_all(engine)
print("Baza danych i relacje zostały utworzone pomyślnie.")


# ===============================================================
# 5. Kod z poprzednich ćwiczeń 
# ===============================================================


# --- Dodawanie i testowanie danych (Ćwiczenia 3) ---
from sqlalchemy import select, update, delete
import random

with Session(engine) as session:
    e1 = Experiment(title="Eksperyment A", type=1)
    e2 = Experiment(title="Eksperyment B", type=2)
    session.add_all([e1, e2])
    session.commit()

    datapoints = [
        DataPoint(real_value=random.uniform(0, 10),
                  target_value=random.uniform(0, 10),
                  experiment_id=e1.id)
        for _ in range(5)
    ]
    session.add_all(datapoints)
    session.commit()

    print("Dane testowe zostały dodane do nowej bazy.")

    Session
