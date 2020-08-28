import dateutil.parser


def parse_iso_string(iso_str: str):
    if not iso_str:
        return None
    return dateutil.parser.parse(iso_str).replace(tzinfo=None, microsecond=0, second=00)
