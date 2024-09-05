def progressbar(current: int, total: int, bar_length: int = 40) -> str:
    progress = current / total
    percent_progress = int(progress * 100)
    block = int(round(bar_length * progress))
    bar = f"{'#' * block + '-' * (bar_length - block)}"
    mid = bar_length // 2
    if bar_length % 2:
        if percent_progress < 10:
            return f'[{bar[0:mid]}{percent_progress}%{bar[mid + 2:]}] {current}/{total}'
        elif percent_progress < 100:
            return f'[{bar[0:mid - 1]}{percent_progress}%{bar[mid + 2:]}] {current}/{total}'
        return f'[{bar[0:mid - 1]}{percent_progress}%{bar[mid + 3:]}] {current}/{total}'

    if percent_progress < 10:
        return f'[{bar[0:mid - 1]}{percent_progress}%{bar[mid + 1:]}] {current}/{total}'
    elif percent_progress < 100:
        return f'[{bar[0:mid - 1]}{percent_progress}%{bar[mid + 2:]}] {current}/{total}'
    return f'[{bar[0:mid - 2]}{percent_progress}%{bar[mid + 2:]}] {current}/{total}'
