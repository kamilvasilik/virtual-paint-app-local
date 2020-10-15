from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from .models import ChosenColors
from .virtual_paint_02 import VirtualPaint02, PickColor

def index(request):
    num_of_colors_defined = len(ChosenColors.objects.all())
    return render(request, 'index.html', {'colorCount': num_of_colors_defined})

def index_select(request):
    if request.method == 'POST':
        hmin = int(request.POST['huemin'])
        hmax = int(request.POST['huemax'])
        smin = int(request.POST['satmin'])
        smax = int(request.POST['satmax'])
        vmin = int(request.POST['valmin'])
        vmax = int(request.POST['valmax'])
        colors = PickColor([hmin, smin, vmin, hmax, smax, vmax])
        print(colors)
        newColor = ChosenColors(huemin=hmin, satmin=smin, valmin=vmin,
                                huemax=hmax, satmax=smax, valmax=vmax,
                                B=colors[0][6], G=colors[0][7], R=colors[0][8])
        newColor.save()
        return render(request, 'index_select.html')
    else:
        return render(request, 'index_select.html')

def how_to_paint(request):
    return render(request, 'how_to_paint.html')

def delete_colors(request):
    old_colors = ChosenColors.objects.all()
    if len(old_colors) != 0:
        for i in range(len(old_colors)):
            to_del = old_colors.get(id=old_colors.first().id)
            to_del.delete()
    return render(request, 'index.html', {'colorCount': len(ChosenColors.objects.all())})


def gen(camera):
    camera.collectColors(ChosenColors.objects.all())
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def vp_draw(request):
    return StreamingHttpResponse(gen(VirtualPaint02()),
                                 content_type="multipart/x-mixed-replace; boundary=frame")
