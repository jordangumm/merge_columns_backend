""" Form Handler Module

A list of uploader helper functions.

"""


def handle_uploaded_file(f):
    with open('uploads/{}'.format(f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)