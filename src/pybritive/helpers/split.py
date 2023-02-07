def profile_split(profile):
    def str_escape_split(str_to_escape, delimiter=',', escape='\\'):
        if len(delimiter) > 1 or len(escape) > 1:
            raise ValueError("Either delimiter or escape must be an one char value")
        token = ''
        escaped = False
        for c in str_to_escape:
            if c == escape:
                if escaped:
                    token += escape
                    escaped = False
                else:
                    escaped = True
                continue
            if c == delimiter:
                if not escaped:
                    yield token
                    token = ''
                else:
                    token += c
                    escaped = False
            else:
                if escaped:
                    token += escape
                    escaped = False
                token += c
        yield token
    return list(str_escape_split(profile, delimiter='/', escape='\\'))
