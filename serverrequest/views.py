from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect 
from base64 import b64decode, b64encode
from DBImage import *
from neyro import *
from PIL import Image
model = init_torch()

def image_as_base64(request):
    if(request.method == 'POST'):
        if((request.POST.get('command')=='Add') & (request.POST.get('upload')!="") & (request.POST.get('title')!="") &
        (request.POST.get('meta')!='')):
            add(request.POST.get('upload'), request.POST.get('title'),request.POST.get('meta'))
            return HttpResponse("Ок")
          
        if((request.POST.get('command')=='Find') & (request.POST.get('upload')!="") & (request.POST.get('title')!="")):
            response = find(request.POST.get('upload'),request.POST.get('title'))
            return JsonResponse({'imageId': response})
        
        if((request.POST.get('command')=='getImage') & (request.POST.get('imageId')!="")):
            image = getImage(request.POST.get('imageId'))
            meta = getMetaInfo(request.POST.get('imageId'))
            return JsonResponse({'image': str(image), 'meta': meta})
          
        return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

index = 0    
def add(upload,title,info):
    image = b64decode(str(upload))
    f=open("media/images/"+str(title),"wb")
    f.write(image)
    f.close()
    input_image = Image.open("media/images/"+str(title))
    descriptor = calc_discriptor(model, input_image)
    data={
        "descriptor": descriptor,
        "meta": str(info)
    }
    AddImage(json.dumps(data),image)

def find(upload,title):
    image = b64decode(str(upload))
    f = open("media/images/" + str(title), "wb")
    f.write(image)
    f.close()
    image_input = Image.open("media/images/"+str(title))
    list = find_images(model, image_input)
    response = []
    for i in list:
        response.append({"image": str(i[1])})
    return response

def getImage(imageId):
    binary = FindImage_new(imageId)
    image = b64encode(binary)
    return image

def getMetaInfo(imageId):
    meta = FindMetaInfo(imageId)
    return meta