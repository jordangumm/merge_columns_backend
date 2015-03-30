from django.http import HttpResponse

def json_response(data, caller):
	""" Streams a json response to the client. """
	from django.core.serializers.json import DjangoJSONEncoder
	from django.db.models.query import ValuesQuerySet
	import json

	if caller == 'upload':
		if str(type(data)) == "<type 'list'>":
			print 'is of type list'
			stream = json.dumps(data, cls=DjangoJSONEncoder)
			return HttpResponse(stream, 'application/json')

	if isinstance(data, ValuesQuerySet):
		print 'is instance'
		def data_stream():
			count = data.count()
			yield '['
			for obj in data.iterator():
				yield json.dumps(obj, cls=DjangoJSONEncoder)
				count -= 1
				if count > 0:
					yield ', '
			yield ']'
		stream = data_stream()
	else:

		print 'else'

		end = []
		for obj in data:
			end.append(obj[1])
		stream = json.dumps(end, cls=DjangoJSONEncoder)

	return HttpResponse(stream, 'application/json')