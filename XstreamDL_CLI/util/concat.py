import platform
from typing import List

ONCE_MAX_FILES = 500


class Concat:

    @staticmethod
    def gen_new_names(names: list, out: str):
        work_num = len(names) // ONCE_MAX_FILES + 1
        counts = len(names) // work_num
        new_names = []
        _tmp_outs = []
        for multi_index in range(work_num):
            if multi_index < work_num - 1:
                _names = names[multi_index * counts:(multi_index + 1) * counts]
            else:
                _names = names[multi_index * counts:]
            _tmp_outs.append(f'out{multi_index}.tmp')
            new_names.append([_names, f'out{multi_index}.tmp'])
        new_names.append([_tmp_outs, out])
        return new_names, _tmp_outs

    @staticmethod
    def gen_cmds_outs(out: str, names: list, raw_concat: bool) -> List[str]:
        cmds = [] # type: List[str]
        if raw_concat is False:
            return [f'ffmpeg -i concat:"{"|".join(names)}" -c copy -y "{out}"'], []
        if len(names) > ONCE_MAX_FILES:
            new_names, _tmp_outs = Concat.gen_new_names(names, out)
            if platform.system() == 'Windows':
                for _names, _out in new_names:
                    cmds.append(f'copy /b {"+".join(_names)} "{_out}"')
                return cmds, _tmp_outs
            else:
                for _names, _out in new_names:
                    cmds.append(f'cat {" ".join(_names)} "{_out}"')
                return cmds, _tmp_outs
        if platform.system() == 'Windows':
            return [f'copy /b {"+".join(names)} "{out}"'], []
        else:
            return [f'cat {" ".join(names)} > "{out}"'], []