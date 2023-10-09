import database
from collections import namedtuple
from typing import AnyStr, List
from enum import Enum, unique

TargetStack = namedtuple('TargetStack', 'course lecture card')


@unique
class Commands(Enum):
    # Course Operations
    add_syllabus = 0x00
    remove_syllabus = 0x01
    reorder_lecture = 0x02

    # Lecture Operations
    add_lecture = 0x10
    remove_lecture = 0x11
    rename_lecture = 0x12
    add_lecture_resource = 0x13
    # remove_lecture_resource = 0x14
    fetch_lecture = 0x15

    # Card Operations
    modify_card_count = 0x20
    modify_card_skipped_flag = 0x21

    # LLM Operations
    fetch_information = 0xF0
    fetch_response = 0xF1


@unique
class StatusCode(Enum):
    success = b'\x00'
    invalid_command = b'\x01'


class Backend:
    def __init__(self, db_path: str, encoding: str = 'utf8'):
        self._encoding = encoding
        self._db = database.IKDatabase(db_path)  # TODO: check type

    def act(self, command: bytes, target_stack: TargetStack, arg: bytes) -> bytes:
        response: StatusCode = StatusCode.success
        match command:
            case Commands.add_syllabus:
                lecture_list = ...  # TODO: call llm interface
                # TODO: add the syllabus
                ...
            case Commands.remove_syllabus:
                # TODO: remove the syllabus
                ...
            case Commands.reorder_lecture:
                # TODO: change the order
                ...
            case Commands.add_lecture:
                lecture_name: str = arg[:128].decode(self._encoding)  # 128-byte string
                lecture_brief: str = arg[128:].decode(self._encoding)
                # TODO: add lecture
                ...
            case Commands.remove_lecture:
                # TODO: remove lecture
                ...
            case Commands.rename_lecture:
                lecture_name_new: str = arg.decode(self._encoding)
                # TODO: rename lecture
                ...
            case Commands.add_lecture_resource:
                resource: List[database.Card] = ...  # TODO: call llm interface (with `arg`)
                # TODO: add cards
                ...
            case Commands.fetch_lecture:
                # TODO: fetch lecture
                # TODO: edit response
                ...
            case Commands.modify_card_count:
                card_count: int = arg[0]
                # TODO: update count
                ...
            case Commands.modify_card_skipped_flag:
                card_flag: bool = bool(arg[0])
                # TODO: update flag
            case Commands.fetch_information:
                subject: str = arg.decode(self._encoding)
                model_response: AnyStr = ...  # TODO: call llm interface (with `subject`)
                # TODO: edit response
            case Commands.fetch_response:
                subject: str = arg.decode(self._encoding)
                model_response: AnyStr = ...  # TODO: call llm interface (with `subject`)
                # TODO: edit response
            case _:
                response = StatusCode.invalid_command

        return response
