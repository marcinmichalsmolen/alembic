# Ćwiczenia praktyczne 5 Alembic


from datetime import datetime, timezone
from sqlalchemy import (
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
)

Base = declarative_base()

subject_experiment_link = Table(
    "subject_experiment_link",
    Base.metadata,
    Column("subject_id", ForeignKey("subject.id"), primary_key=True),
    Column("experiment_id", ForeignKey("experiment.id"), primary_key=True),
)



class Experiment(Base):
    __tablename__ = "experiment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)  
    )
    type: Mapped[int] = mapped_column(Integer)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)

    data_points: Mapped[list["DataPoint"]] = relationship(
        back_populates="experiment", cascade="all, delete-orphan"
    )
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=subject_experiment_link,  
        back_populates="experiments",
    )


class DataPoint(Base):
    __tablename__ = "datapoint"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    experiment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("experiment.id"), nullable=False
    )
    experiment: Mapped["Experiment"] = relationship(back_populates="data_points")

class Subject(Base):
    __tablename__ = "subject"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gdpr_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    experiments: Mapped[list["Experiment"]] = relationship(
        secondary=subject_experiment_link, back_populates="subjects"  
    )