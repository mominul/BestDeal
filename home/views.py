from multiprocessing import Process
from django.shortcuts import render

from .ryans import scrape_ryans
from .daraz import scrape_daraz

def home(request):
    if request.POST:
        search = request.POST["search"]

        ryans = scrape_ryans(search)
        daraz = scrape_daraz(search)

        items = []
        items += ryans
        items += daraz

        data = {
            "items": items,
        }
        return render(request, 'result.html', data)
    return render(request, 'home.html')


def run_cpu_tasks_in_parallel(tasks):
    running_tasks = [Process(target=task) for task in tasks]
    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        running_task.join()