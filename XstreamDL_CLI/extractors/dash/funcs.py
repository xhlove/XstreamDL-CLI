import re
from typing import Dict

from .links import Links


def tree(obj, step: int = 0):
    print(f"{step * '--'}>{obj.name}")
    step += 1
    for child in obj.childs:
        step = tree(child, step=step)
    step -= 1
    print(f"{step * '--'}>{obj.name}")
    return step


def find_child(name: str, parent):
    return [child for child in parent.childs if child.name == name]


def dump(tracks: Dict[str, Links]):
    for track_key, links in tracks.items():
        links.dump_urls()


def match_duration(_duration):
    if isinstance(_duration, str) is False:
        return

    duration = re.match(r"PT(\d+)(\.?\d+)S", _duration)
    if duration is not None:
        return float(duration.group(1)) if duration else 0.0
    # P0Y0M0DT0H3M30.000S
    duration = re.match(r"PT(\d+)H(\d+)M(\d+)(\.?\d+)S",
                        _duration.replace('0Y0M0D', ''))
    if duration is not None:
        _h, _m, _s, _ss = duration.groups()
        return int(_h) * 60 * 60 + int(_m) * 60 + int(_s) + float("0" + _ss)