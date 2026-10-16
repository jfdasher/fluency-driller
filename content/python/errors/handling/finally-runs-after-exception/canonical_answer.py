def safe_divide(a, b, log):
    try:
        result = a / b
    except ZeroDivisionError:
        result = None
    finally:
        log.append('done')
    return result
