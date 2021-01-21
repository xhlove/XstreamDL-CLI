from enum import Enum


class VideoCodecs(Enum):
    H264 = 1
    H265 = 2
    VP9 = 3
    AV1 = 4


class AudioCodecs(Enum):
    AAC = 1
    AC3 = 2