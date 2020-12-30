from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import *
from django.db.models import F
from django.http import JsonResponse
import json
import datetime
# from io import StringIO
from . utils import cookiePanier, panierData, guestCommande
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def main(request):
	context = {}
	return render(request,'boutique/main.html', context)


def accueil(request):

	data = panierData(request)
	panierArticles = data['panierArticles']

	tuniques = Produit.objects.order_by(F("id").desc(nulls_last=True)).filter(typee = "tunique")[:20]
	accessoires = Produit.objects.order_by(F("id").desc(nulls_last=True)).filter(typee = "accessoire")[:20]
	aliments = Produit.objects.order_by(F("id").desc(nulls_last=True)).filter(typee = "aliment")[:20]
	context = {'tuniques':tuniques,'accessoires':accessoires, 'aliments':aliments,'panierArticles':panierArticles}
	return render(request,'boutique/accueil.html', context)


def tunique(request):
	
	data = panierData(request)
	panierArticles = data['panierArticles']

	tuniques = Produit.objects.order_by(F("id").desc(nulls_last=True)).filter(typee = "tunique")

	paginator = Paginator(tuniques, per_page=40)
	page_number = request.GET.get('page', 1)
	page_obj = paginator.get_page(page_number)

	context = {'tuniques':page_obj.object_list,'panierArticles':panierArticles,'paginator':paginator,'page_number':int(page_number)}

	return render(request,'boutique/tunique.html', context)


def accessoirs(request):

	data = panierData(request)
	panierArticles = data['panierArticles']

	accessoires = Produit.objects.order_by(F("id").desc(nulls_last=True)).filter(typee = "accessoire")

	paginator = Paginator(accessoires, per_page=40)
	page_number = request.GET.get('page', 1)
	page_obj = paginator.get_page(page_number)

	context = {'accessoires':accessoires,'panierArticles':panierArticles,'paginator':paginator,'page_number':int(page_number)}
	return render(request,'boutique/accessoirs.html', context)


def panier(request):
	data = panierData(request)
	panierArticles = data['panierArticles']
	commande = data['commande']
	articles = data['articles']
		


	context = {"articles":articles,"commande":commande,"panierArticles":panierArticles}
	return render(request,'boutique/panier.html', context)



def acheter(request):

	data = panierData(request)
	panierArticles = data['panierArticles']
	commande = data['commande']
	articles = data['articles']
		
	context = {"articles":articles,"commande":commande,"panierArticles":panierArticles}
	return render(request,'boutique/acheter.html', context)


def alimentation(request):

	data = panierData(request)
	panierArticles = data['panierArticles']

	aliments = Produit.objects.order_by(F("id").desc(nulls_last=True)).filter(typee = "aliment")

	paginator = Paginator(aliments, per_page=40)
	page_number = request.GET.get('page', 1)
	page_obj = paginator.get_page(page_number)

	context = {'aliments':aliments,'panierArticles':panierArticles,'paginator':paginator,'page_number':int(page_number)}
	return render(request,'boutique/alimentation.html', context)


def updateArticle(request):
	data = json.loads(request.body)
	produitId = data['produitId']
	action = data['action']

	print('Action:',action)
	print('Produit:',produitId)

	client = request.user.client
	produit = Produit.objects.get(id=produitId)
	commande, created = Commande.objects.get_or_create(client=client, complete=False)

	commandeArticle, created = CommandeArticle.objects.get_or_create(commande=commande, produit=produit)

	if action == 'add':
		commandeArticle.quantite = (commandeArticle.quantite + 1)
	elif action == 'remove':
		commandeArticle.quantite = (commandeArticle.quantite - 1)

	commandeArticle.save()

	if commandeArticle.quantite <= 0:
		commandeArticle.delete()

	return JsonResponse('L\'article est ajouté', safe=False)


def processCommande(request):
	transactionId = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		client = request.user.client
		commande, created = Commande.objects.get_or_create(client=client, complete=False)

	else:
		client, commande = guestCommande(request, data)


	total = float(data['form']['total'])
	commande.transactionId = transactionId

	if total == commande.get_panier_total:
		commande.complete = True
	commande.save()

	if commande.livraison == True:
		LivraisonAdresse.objects.create(
			client = client,
			commande = commande,
			adresse = data['livraison']['adresse'],
			region = data['livraison']['region'],
			pays = data['livraison']['pays'],
			telephone = data['livraison']['telephone'],
		)

	# print('data :',request.body)
	return JsonResponse('Payment complet!', safe=False)
	
	