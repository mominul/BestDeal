from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .generate_chat import chatgen
from .models import ChatHistory


def chat_home(request):
    if request.method == 'POST':
        chat = request.POST["chat"]
        response = chatgen(chat).removeprefix("1. ")
        history = ChatHistory(prompt=chat, response=response)
        history.save()
        return redirect('chat_home')

    history = ChatHistory.objects.all()
    items = []
    for item in history:
        items.append({
            "prompt": item.prompt,
            "response": item.response,
        })
    
    # Check if the 'items' list is not empty before accessing its last item
    if items:
        request.session["data"] = items[-1]["response"]
    else:
        request.session["data"] = ""  # Set a default value if 'items' is empty

    data = {
        "history": items,
    }

    return render(request, 'chat_home.html', data)


def chat_clear(request):
    ChatHistory.objects.all().delete()
    return redirect('chat_home')
