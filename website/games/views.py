from django.shortcuts import render

# Create your views here.
def games(request):
    return render(request, 'games.html')

def mem_pat(request):
    return render(request, 'mem_pat.html')

def reaction(request):
    return render(request, 'reaction.html')

def lung_game(request):
    return render(request, 'lung_game.html')