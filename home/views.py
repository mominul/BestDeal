from multiprocessing import Process
from django.shortcuts import render

from .ryans import scrape_ryans
from .daraz import scrape_daraz

def home(request):
    if request.POST:
        search = request.POST["search"]

        ryans = scrape_ryans(search)
        daraz = scrape_daraz(search)

        # Create an array containing 'ryans' and 'daraz' data
        result_array = [ryans, daraz]
        # Store the array in the session
        request.session['result_array'] = result_array

        data = {
            "ryans": ryans,
            "daraz": daraz,
        }
        return render(request, 'result.html', data)
    return render(request, 'home.html')

def filter_items(request):
    if request.POST:
        max_price=request.POST["max_price"]
        filtered_items = []
        result_array= request.session['result_array']
        for site_data in result_array:
            site_filtered_items = []
            if site_data['price'] <= max_price:
                site_filtered_items.append(site_data)
                filtered_items.append(site_filtered_items)
    
        return render(request, 'result.html', filtered_items)
    return render(request, 'home.html')   

def run_cpu_tasks_in_parallel(tasks):
    running_tasks = [Process(target=task) for task in tasks]
    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        running_task.join()