from django.shortcuts import render
import json
from strsimpy.jaro_winkler import JaroWinkler

def home(request):
    if request.POST:
        search = request.POST["search"]

        data = {
            "query": search,
        }
        return render(request, 'result03.html', data)
    
    return render(request, 'home02.html')

def compare(request):
    data = request.POST["jsonData"]
    data = json.loads(data)

    jarowinkler = JaroWinkler()

    similarity = {}

    for idx1, s1 in enumerate(data):
        t1 = s1["title"].lower()
        for idx2, s2 in enumerate(data):
            # Skip same products
            if s1 == s2:
                continue
            # Skip products from same dealer
            if s1["logo"] == s2["logo"]:
                continue

            t2 = s2["title"].lower()
            score = jarowinkler.similarity(t1, t2)

            if score > 0.8:
                if similarity.get(idx1):
                    similarity[idx1].append({
                        "related": idx2,
                        "score": score,
                    })
                else:
                    similarity[idx1] = [{
                        "related": idx2,
                        "score": score,
                    }]

    similarity2 = {}
    visited = []
    for key, value in similarity.items():
        if (not key in similarity2) and (not key in visited):
            similarity2[key] = value

            for item in value:
                product = item["related"]
                if product == key:
                    continue
                if (product in similarity.keys()) and (not product in visited):
                    related = similarity[product]
                    similarity2[key] += related
                    visited.append(product)

    similarity3 = {}
    
    added = []

    for key, value in similarity2.items():
        similarity3[key] = []
        for item in value:
            product = item["related"]
            # Skip same product
            if product == key:
                continue
            # Skip already added product
            if product in added:
                continue

            similarity3[key].append(item)
            added.append(product)

    indexes = []
    segments = []

    for key, value in similarity3.items():
        segment = []
        segment.append(data[key])
        indexes.append(key)
        for product in value:
            segment.append(data[product["related"]])
            indexes.append(data[product["related"]])
        
        segments.append(segment)

    # Sort the products by price in segments
    for idx, product in enumerate(segments):
        product.sort(key=price)
        segments[idx] = product

    leftover = []

    for index, product in enumerate(data):
        if not index in indexes:
            leftover.append(product)
    
    response = {
        "segments": segments,
        "leftover": leftover
    }

    return render(request, "compare.html", response)

def price(product):
    string = product["price"]
    string = string.replace("৳", "")
    string = string.replace("Tk", "")
    string = string.replace(",", "")
    string.strip()
    return int(string)
