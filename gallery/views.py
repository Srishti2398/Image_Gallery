from io import StringIO
from PIL.Image import Image
from django.core import paginator
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from .models import Category, Photo

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def gallery(request):

    categories = Category.objects.all()
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)
    
    
    
    photo_paginator = Paginator( photos, 4)

    page_num = request.GET.get('page')

    page = photo_paginator.get_page(page_num)



    

    context = {'categories': categories,  'page': page }
    return render(request, 'gallery/home.html', context)


def viewphoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'gallery/view.html', {'photo': photo})


def rotateLeft(request,pk):
    categories = Category.objects.all()
    photo = Photo.objects.get(id=pk)

    original_photo = StringIO.StringIO(Photo.file.read())
    rotated_photo = StringIO.StringIO()

    photos = Image.open(original_photo)
    image = photos.rotate(-90)
    image.save(rotated_photo, 'JPEG')

    photo.file.save(image.file.path, ContentFile(rotated_photo.getvalue()))
    photo.save()
    context = {'categories': categories,  'photo': photo }
    return render(request, 'gallery/home.html', context)


def addphoto(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        data =request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category =Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')


    context = {'categories': categories}
    
    return render(request, 'gallery/add.html',context)