from channels.generic.websocket import JsonWebsocketConsumer
from multiprocessing import Process, Queue
from .ryans import scrape_ryans
from .daraz import scrape_daraz
from .startech import scrape_startech
from .pickaboo import scrape_pickaboo

def scrape_website(query, website_func, results_queue):
    try:
        results = website_func(query)
    except Exception as e:
        print('[Search Websocket] Exception occurred while scrapping!', e)
        pass

    results_queue.put(results)

class SearchConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive_json(self, content):
        query = content['query']

        # Create a multiprocessing queue to collect the results
        results_queue = Queue()

        tasks = [
            Process(target=scrape_website, args=(query, scrape_ryans, results_queue)),
            Process(target=scrape_website, args=(query, scrape_daraz, results_queue)),
            Process(target=scrape_website, args=(query, scrape_startech, results_queue)),
            Process(target=scrape_website, args=(query, scrape_pickaboo, results_queue)),
        ]

        for task in tasks:
            task.start()
        
        sources = 0
        while sources < len(tasks):
            try:
                items = results_queue.get()
                # Send the data
                self.send_json(content={
                    "type": "data",
                    "items": items
                })
                sources += 1
            except:
                print("[Search websocket] An exception is thrown")
                pass

        # We have finished getting all the results, so send a finish notification
        self.send_json(content={
            "type": "finished",
        })

        for task in tasks:
            task.join()

