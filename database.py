from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from typing import List

Base = declarative_base()


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    syllabus = Column(String)
    lectures = relationship("Lecture", back_populates="course")


class Lecture(Base):
    __tablename__ = "lectures"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    resources = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="lectures")
    cards = relationship("Card", back_populates="lecture")


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    skipped = Column(Boolean, default=False)
    presence_count = Column(Integer, default=0)
    lecture_id = Column(Integer, ForeignKey("lectures.id"))
    lecture = relationship("Lecture", back_populates="cards")


class IKDatabase:
    def __init__(self, db_url="sqlite:///iknowledge_db.sqlite"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_course(self, course: Course):
        with self.Session.begin() as session:
            session.add(course)

    def add_slides_to_course(self, course_id: int, slides: List[str]):
        with self.Session.begin() as session:
            course = session.query(Course).filter(Course.id == course_id).one_or_none()
            if course:
                course.resources.extend(slides)

    def remove_course(self, course_id: int):
        with self.Session.begin() as session:
            course = session.query(Course).filter(Course.id == course_id).one()
            session.delete(course)

    def add_lecture(self, course_id: int, lecture: Lecture):
        with self.Session.begin() as session:
            course = session.query(Course).filter(Course.id == course_id).one_or_none()
            if course:
                course.lectures.append(lecture)

    def remove_lecture(self, lecture_id: int):
        with self.Session.begin() as session:
            lecture = session.query(Lecture).filter(Lecture.id == lecture_id).one()
            session.delete(lecture)

    def rename_lecture(self, lecture_id: int, new_title: str):
        with self.Session.begin() as session:
            lecture = (
                session.query(Lecture).filter(Lecture.id == lecture_id).one_or_none()
            )
            if lecture:
                lecture.title = new_title

    def reorder_lectures(self, course_id: int, new_order: List[int]):
        with self.Session.begin() as session:
            course = session.query(Course).filter(Course.id == course_id).one_or_none()
            if course:
                course.lectures.sort(key=lambda x: new_order.index(x.id))

    def add_resources_to_lecture(self, lecture_id: int, resources: List[str]):
        with self.Session.begin() as session:
            lecture = (
                session.query(Lecture).filter(Lecture.id == lecture_id).one_or_none()
            )
            if lecture:
                lecture.resources.extend(resources)

    def remove_resources_from_lecture(self, lecture_id: int, resources: List[str]):
        with self.Session.begin() as session:
            lecture = (
                session.query(Lecture).filter(Lecture.id == lecture_id).one_or_none()
            )
            if lecture:
                for resource in resources:
                    lecture.resources.remove(resource)

    def mark_card_skipped(self, card_id: int):
        with self.Session.begin() as session:
            card = session.query(Card).filter(Card.id == card_id).one_or_none()
            if card:
                card.skipped = True

    def update_card_presence_count(self, card_id: int, count: int):
        with self.Session.begin() as session:
            card = session.query(Card).filter(Card.id == card_id).one_or_none()
            if card:
                card.presence_count = count


if __name__ == "__main__":
    db_interface = IKDatabase()

    course = Course(
        title="CS101",
        syllabus="Lecture 1 Introduction to CS\nLecture 2 Cervical Spondylosis Rehabilitation Guide",
    )
    lecture = Lecture(title="Introduction to CS")
    card = Card(content="Some card content")

    lecture.cards.append(card)
    course.lectures.append(lecture)

    db_interface.add_course(course)

    db_interface.mark_card_skipped(1)
    db_interface.update_card_presence_count(1, 1)
