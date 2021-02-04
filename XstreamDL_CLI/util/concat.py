class Concat:

    @staticmethod
    def gen_cmd(out: str, names: list):
        return f'ffmpeg -i concat:"{"|".join(names)}" -c copy -y "{out}"'