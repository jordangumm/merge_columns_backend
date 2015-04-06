from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import UploadFileForm
from util.util import json_response
from pickle import load
from AutomaticClusterLabels.DoGrouping import MergeSpreadsheet
import simplejson


def upload_file(request):
    print 'uploading file...'
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            print "valid"
            handle_uploaded_file(request.FILES['file'])

            return render_to_response('success.html', context_instance=RequestContext(request))
        else:
            print "form is not valid"
            return render_to_response('index.html')
    else:
        print 'upload is not a post!'



def index(request):
    print 'loading index...'
    return render_to_response('index.html')


def handle_uploaded_file(f):
    print 'handling uploaded file...'
    try:
        with open('/var/www/uploads/files/{}'.format(f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    except Exception as e:
        print 'handle_uploaded_file: {}'.format(e)
      
def merge_files(output_name):
    import os
    
    files = os.listdir('/var/www/uploads/files/')
    final_files = []
    for i, the_file in enumerate(files):
        if the_file.endswith('.csv') and not the_file.endswith('-values.csv'): # only accept csv files
            final_files.append('/var/www/uploads/files/{}'.format(the_file))
    
    try:
        dg = MergeSpreadsheet()
    except Exception as e:
        print 'Exception in MergeSpreadsheet(): {}'.format(e)

    try:
        dAllCombos = dg.getAllScores(final_files)
    except Exception as e:
        print 'Exception in getAllScores(): {}'.format(e)
        print 'files: {}'.format(final_files)

    try:
        lsMerged,lsAlone = dg.doGrouping(dAllCombos)
    except Exception as e:
        print 'Exception in doGrouping(): {}'.format(e)

    for the_file in final_files:
        try:
            if os.path.isfile(the_file):
                os.unlink(the_file)
        except Exception as e:
            print 'Exception when unlinking file: {}'.format(e)

    try:
        dg.writeSpreadsheet(lsMerged,lsAlone, output_name)
    except Exception as e:
        print 'Exception in writeSpreadsheet: {}'.format(e)

    return


def process_files(request):
    try:
        print 'processing files...'
        output_name = request.GET['output_name']
    
        print 'merging files...'
        merge_files(output_name)
    
        print 'returning...'
        return json_response(['Success'], 'upload')
    except Exception as e:
        print 'process_files Exception: {}'.format(e)
        return json_response(['Failure'], 'upload')
    
    
    
