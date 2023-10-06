import database
from collections import namedtuple
from typing import AnyStr, List

ENCODING = 'utf8'

TargetStack = namedtuple('TargetStack', 'course lecture card')


class Commands:
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


class StatusCode:
    success = b'\x00'
    invalid_command = b'\x01'


class Backend:
    def __init__(self, db_path: AnyStr):
        self.db = database.IKDatabase(db_path)  # TODO: check type

    def act(self, command: bytes, target_stack: TargetStack, arg: bytes) -> bytes:
        response: bytes = StatusCode.success
        if command == Commands.add_syllabus:
            lecture_list = ...  # TODO: call llm interface
            # TODO: add the syllabus
            ...
        elif command == Commands.remove_syllabus:
            # TODO: remove the syllabus
            ...
        elif command == Commands.reorder_lecture:
            # TODO: change the order
            ...
        elif command == Commands.add_lecture:
            lecture_name: str = arg[:128].decode(ENCODING)  # 128-byte string
            lecture_brief: str = arg[128:].decode(ENCODING)
            # TODO: add lecture
            ...
        elif command == Commands.remove_lecture:
            # TODO: remove lecture
            ...
        elif command == Commands.rename_lecture:
            lecture_name_new: str = arg.decode(ENCODING)
            # TODO: rename lecture
            ...
        elif command == Commands.add_lecture_resource:
            resource: List[database.Card] = ...  # TODO: call llm interface (with `arg`)
            # TODO: add cards
            ...
        elif command == Commands.fetch_lecture:
            # TODO: fetch lecture
            # TODO: edit response
            ...
        elif command == Commands.modify_card_count:
            card_count: int = arg[0]
            # TODO: update count
            ...
        elif command == Commands.modify_card_skipped_flag:
            card_flag: bool = bool(arg[0])
            # TODO: update flag
        elif command == Commands.fetch_information:
            subject: str = arg.decode(ENCODING)
            model_response: AnyStr = ...  # TODO: call llm interface (with `subject`)
            # TODO: edit response
        elif command == Commands.fetch_response:
            subject: str = arg.decode(ENCODING)
            model_response: AnyStr = ...  # TODO: call llm interface (with `subject`)
            # TODO: edit response
        else:
            response = StatusCode.invalid_command

        return response
