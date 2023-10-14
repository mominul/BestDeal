from django.shortcuts import render

def home(request):
    if request.POST:
        search = request.POST["search"]

        data = {
            "query": search,
        }
        return render(request, 'result03.html', data)
    
    return render(request, 'home02.html')
