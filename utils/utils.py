
from datetime import datetime
import time
import enum
import uuid
from decimal import Decimal


def prepare_update_object(new_data, old_data, updated_from, geo_loc, has_history: bool = True) -> dict:
    update = {'update_history': []} if has_history else {}
    update_history_old = {}
    update_history_new = {}

    for attr in new_data.__fields__.keys():
        value = getattr(new_data, attr)
        prev_value = getattr(old_data, attr)

        if value is not None and attr != 'update_history' and attr != 'version':
            if is_custom_type(value):
                upd = sub_update(value, old_data, update_history_old, update_history_new, attr, has_history)
                if upd is not None:
                    update.update(upd)
            elif isinstance(value, list):
                olds = [i.dict(exclude_unset=True) for i in getattr(old_data, attr) if i not in value]
                update[attr] = [item.dict(exclude_unset=True) for item in value] + olds
                if has_history:
                    update_history_old[attr] = olds
                    update_history_new[attr] = update[attr]

            elif value != prev_value:
                update[attr] = str(value) if isinstance(value, Decimal) else value
                if has_history:
                    update_history_old[attr] = prev_value
                    update_history_new[attr] = update[attr]

    if has_history:
        update['update_history'].append({
            'timestamp': int(time.time()),
            'updated_from': updated_from,
            'geo_loc': geo_loc,
            'old_values': update_history_old,
            'new_values': update_history_new
        })

        if old_data.update_history:
            update['update_history'] += old_data.update_history

    return update


def sub_update(value, old_data, update_history_old, update_history_new, attr, has_history: bool = True) -> dict:
    sub_update = None
    if hasattr(value, '__fields__'):
        sub_update = {}
        if has_history:
            update_history_old[attr] = {}
            update_history_new[attr] = {}

        for sub_attr, sub_value in value.dict(exclude_unset=True).items():
            prev_sub_value = getattr(getattr(old_data, attr), sub_attr, "")

            if sub_value is not None and sub_value != prev_sub_value:
                sub_update[f"{attr}.{sub_attr}"] = sub_value
                if has_history:
                    update_history_old[attr][sub_attr] = prev_sub_value
                    update_history_new[attr][sub_attr] = sub_value
    return sub_update


def is_custom_type(value) -> bool:
    primitives = (int, float, str, bool, type(None), list, dict)
    other_types = (datetime, uuid.UUID, enum.Enum, Decimal)
    return not isinstance(value, primitives + other_types) and not issubclass(type(value), enum.Enum)
