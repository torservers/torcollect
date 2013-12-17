def application(environment, start_response):
    response_body = ["<html><head><title>test</title></head>\
                      <body><h1>ohai<h1></body></html>"]
    response_headers = []

    content_length = 0
    for s in response_body:
        content_length += len(s)
    response_headers.append(('Content-Length', str(content_length)))
    response_headers.append(('Content-Type', 'text/html'))
    status = '200 OK'
    start_response(status, response_headers)
    return response_body
