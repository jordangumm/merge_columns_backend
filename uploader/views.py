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
    with open('files/{}'.format(f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
 
      
def merge_files(output_name):
    import os
    
    files = os.listdir('files/')
    final_files = []
    for i, the_file in enumerate(files):
        if the_file.endswith('.csv'): # only accept csv files
            final_files.append('files/{}'.format(the_file))
    
    print 'making MergeSpreadsheet object...'
    dg = MergeSpreadsheet()
    print files
    
    print 'getting all scores...'
    dAllCombos = dg.getAllScores(final_files)
    
    print 'grouping...'
    lsMerged,lsAlone = dg.doGrouping(dAllCombos)
    
    print 'writing...'
    dg.writeSpreadsheet(lsMerged,lsAlone, output_name)
    
    print 'removing old files...'
    for the_file in final_files:
        if os.path.isfile(the_file):
            os.remove(the_file)
    
    return


def process_files(request):
    print 'processing files...'
    output_name = request.GET['output_name']
    
    print 'merging files...'
    merge_files(output_name)
    
    print 'returning...'
    return json_response(['Success'], 'upload')
    
    
    
    