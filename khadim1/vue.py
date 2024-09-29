from django.http import HttpResponse
from django.shortcuts import render




def main(request):
	context = {}
	return render(request,'main.html', context)

def accueil(request):
	context = {}
	return render(request,'accueil.html', context)

def tunique(request):
	context = {}
	return render(request,'tunique.html', context)

def boss(request):
	context = {}
	return render(request,'boss.html', context)

def accessoirs(request):
	context = {}
	return render(request,'accessoirs.html', context)

def panier(request):
	context = {}
	return render(request,'panier.html', context)

def acheter(request):
	context = {}
	return render(request,'acheter.html', context)