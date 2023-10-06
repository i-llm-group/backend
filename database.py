from tinydb import TinyDB, Query


class Course:
    def __init__(self, title, syllabus):
        self.title = title
        self.syllabus = syllabus
        self.lectures = []

    def add_lecture(self, lecture):
        self.lectures.append(lecture)

    def remove_lecture(self, lecture):
        self.lectures.remove(lecture)

    def serialize(self):
        return {
            "title": self.title,
            "syllabus": self.syllabus,
            "lectures": [lecture.serialize() for lecture in self.lectures],
        }

    @staticmethod
    def deserialize(data):
        course = Course(data["title"], data["syllabus"])
        course.lectures = [
            Lecture.deserialize(lecture_data) for lecture_data in data["lectures"]
        ]
        return course


class Lecture:
    def __init__(self, title):
        self.title = title
        self.resources = []
        self.cards = []

    def add_resource(self, resource):
        self.resources.append(resource)

    def remove_resource(self, resource):
        self.resources.remove(resource)

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def serialize(self):
        return {
            "title": self.title,
            "resources": self.resources,
            "cards": [card.serialize() for card in self.cards],
        }

    @staticmethod
    def deserialize(data):
        lecture = Lecture(data["title"])
        lecture.resources = data["resources"]
        lecture.cards = [Card.deserialize(card_data) for card_data in data["cards"]]
        return lecture


class Card:
    def __init__(self, skipped=False, count=0):
        self.skipped = skipped
        self.count = count

    def serialize(self):
        return {"skipped": self.skipped, "count": self.count}

    @staticmethod
    def deserialize(data):
        return Card(data["skipped"], data["count"])


class IKDatabase:
    def __init__(self, db_path="iknowledge_db.json"):
        self.db = TinyDB(db_path)

    def add_course(self, course):
        self.db.table("Courses").upsert(
            course.serialize(), Query().title == course.title
        )

    def get_course(self, title):
        course_data = self.db.table("Courses").get(Query().title == title)
        if course_data:
            return Course.deserialize(course_data)
        return None

    def remove_course(self, title):
        self.db.table("Courses").remove(Query().title == title)


# Usage:
ik_db = IKDatabase()
course = Course("CS101", "Introduction to CS")
lecture = Lecture("Lecture 1")
lecture.add_resource("Slide 1")
card = Card()
lecture.add_card(card)
course.add_lecture(lecture)
ik_db.add_course(course)  # Now adding course to the database

# Retrieving course from the database
retrieved_course = ik_db.get_course("CS101")
