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
        items = []
        items += ryans
        items += daraz

        # Store the array in the session
        request.session['result_array'] = items

        data = {
            "items": items,
        }
        return render(request, 'result.html', data)
    return render(request, 'home.html')

def filter_items(request):
    if request.POST:
        max_price=request.POST["max_price"]
        filtered_items = []
        result_array= request.session['result_array']

        print(result_array)
        for site_data in result_array:
            if site_data['price'] <= max_price:
                filtered_items.append(site_data)

        filtered_items = sort_items_by_price(filtered_items)

        data = {
            'items':filtered_items
        }
        return render(request, 'result.html', data)
    # print(request.POST['max_price'])
    return render(request, 'home.html')   

def sort_items_by_price(filtered_items):
    # Sort the filtered_items list in ascending order based on 'price'
    sorted_items = sorted(filtered_items, key=lambda x: x['price'])
    return sorted_items

def run_cpu_tasks_in_parallel(tasks):
    running_tasks = [Process(target=task) for task in tasks]
    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        running_task.join()