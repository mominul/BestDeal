from django.shortcuts import render

from .ryans import scrape_ryans

def home(request):
    if request.POST:
        search = request.POST["search"]
        items = scrape_ryans(search)

        data = {
            "items": items
        }
        return render(request, 'result.html', data)
    return render(request, 'home.html')
