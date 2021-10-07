def load_raw2text(data: bytes):
    raw_text = None # type: str
    try:
        raw_text = data.decode('utf-8')
    except UnicodeDecodeError:
        try:
            raw_text = data.decode('utf-16')
        except Exception as e:
            print(f'err => {e}')
    return raw_text