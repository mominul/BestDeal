from multiprocessing import Process, Queue
from django.shortcuts import render

from .ryans import scrape_ryans
from .daraz import scrape_daraz
from .startech import scrape_startech
from .pickaboo import scrape_pickaboo

def scrape_website(query, website_func, results_queue):
    results = website_func(query)
    results_queue.put(results)


def home(request):
    if request.POST:
        search = request.POST["search"]

        # Create a multiprocessing queue to collect the results
        results_queue = Queue()

        
        tasks = [
            Process(target=scrape_website, args=(search, scrape_ryans, results_queue)),
            Process(target=scrape_website, args=(search, scrape_daraz, results_queue)),
            Process(target=scrape_website, args=(search, scrape_startech, results_queue)),
            Process(target=scrape_website, args=(search, scrape_pickaboo, results_queue)),
        ]


        for task in tasks:
            task.start()
        for task in tasks:
            task.join()

        items = []
        # # items += ryans
        # # items += daraz
        # # items += startech
        # items += pickaboo

        while not results_queue.empty():
            items += results_queue.get()

        data = {
            "items": items,
        }
        return render(request, 'result02.html', data)
    
    return render(request, 'home02.html')
