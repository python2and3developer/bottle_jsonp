from bottle import request, response, json_dumps


APPLICATION_JS = 'application/javascript'

JSONP_TEMPLATE = u'{callback}({payload})'

JSONP = 'jsonp'
CALLBACK = 'callback'


def get_callback():
    return request.GET.get(CALLBACK, request.GET.get(JSONP, None))


def jsonp(callback):
    def wrapper(*a, **ka):

        data = callback(*a, **ka)

        jsonp_callback = get_callback()
        if jsonp_callback is not None:
            payload = json_dumps(data)

            # Set content type
            response.content_type = APPLICATION_JS

            wrapped_payload = JSONP_TEMPLATE.format(
                callback=jsonp_callback,
                payload=payload)

            return wrapped_payload
        else:
            return data

    return wrapper
