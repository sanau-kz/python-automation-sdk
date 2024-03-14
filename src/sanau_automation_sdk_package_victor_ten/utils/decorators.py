def catch(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        headers = kwargs.get('headers', {})
        kwargs['headers'] = {**self.access_key, **headers}

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            return e
        return result

    return wrapper
