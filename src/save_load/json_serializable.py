import typing

import src
import json
from typing import Any
from abc import ABC, abstractmethod

def is_json_serializable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False

class JsonSerializable(ABC):
    deserialize_dict_obj_map = {}

    def __init__(self, deserialize_tag : str = None):
        if not deserialize_tag:
            deserialize_tag = self.__class__.__name__
        JsonSerializable.deserialize_dict_obj_map[deserialize_tag] = self.__class__

        self.deserialize_tag = deserialize_tag

    def serialize(self) -> dict[str, Any]:
        print(f" --- SERIALIZING {self.__class__.__name__} --- ")
        return self.serialize_recurse(self)

    def serialize_recurse(self, obj : dict):
        if isinstance(obj, dict):
            obj_dict = dict(obj)
        else:
            obj_dict = dict(obj.__dict__)

        for key, value in obj_dict.items():
            if isinstance(value, JsonSerializable):
                obj_dict[key] = value.serialize()
            elif isinstance(value, list):
                obj_dict[key] = [self.serialize_recurse(i) for i in value]
            elif isinstance(value, dict):
                obj_dict[key] = self.serialize_recurse(value)

            elif not is_json_serializable(value):
                obj_dict[key] = "Could not parse."

        return obj_dict

    def deserialize(self, obj_dict : dict[str, Any]):
        print(f" --- DESERIALIZING {self.__dict__["deserialize_tag"]} --- ")
        return self.deserialize_recurse(obj_dict)

    def deserialize_recurse(self, obj_dict : dict[str, Any]):

        for key in obj_dict:
            value = obj_dict[key]

            if isinstance(value, list):
                obj_dict[key] = [self.deserialize_recurse(i) for i in value]
            elif isinstance(value, dict):
                obj_dict[key] = self.deserialize_recurse(value)

            try:
                value_inst = JsonSerializable.deserialize_dict_obj_map[value["deserialize_tag"]]()
                value_inst.deserialize(value)
                obj_dict[key] = value_inst
            except (TypeError, KeyError) as e:
                # print(f"Error : {e}")
                pass

        self.__dict__ = obj_dict