#!/usr/bin/python
#-*- coding:utf-8 -*-


def generate_daytable(day):
    pass


def application(environment, start_response):
    response_body = ["<html><head><title>test</title></head>\
                      <body><h1>ohai<h1></body></html>"]
    response_headers = []

    if environment["PATH_INFO"] == '/':
        # Output Mainpage
        pass
    elif environment["PATH_INFO"].begins("/day/"):
        # Output Dayly page
        import torcollect.web.cache
        if not torcollect.web.cache.has(environment["PATH_INFO"]):
            torcollect.web.cache.create(environment["PATH_INFO"])

        response_body.append(
            torcollect.web.cache.get(environment["PATH_INFO"])
        )

    content_length = 0
    for s in response_body:
        content_length += len(s)
    response_headers.append(('Content-Length', str(content_length)))
    response_headers.append(('Content-Type', 'text/html'))
    status = '200 OK'
    start_response(status, response_headers)
    return response_body
