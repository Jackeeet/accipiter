def duplicated_param(param_name: str):
    return f"[Параметр инструмента] Параметр '{param_name}' уже указан"


def extra_symbols():
    return "Обнаружены дополнительные символы"


def unsupported_block(block_kind):
    return f"Неподдерживаемый тип блока: {block_kind}"


def unsupported_processing_type():
    return f"Ожидалось действие или событие"


def unexpected_token(token, location: str = None):
    loc_string = f"[{location}] " if location else ""
    return f"{loc_string}Неожиданный токен: {token.kind}"
