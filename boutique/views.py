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
# import paydunya
# from paydunya import Store, InvoiceItem




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
		
	# print('Prenom ', data['form']['prenom'])
	# print('Nom ', data['form']['nom'])


	# print('data :',request.body)
	return JsonResponse('Payment complet!', safe=False)
	
	


def processPaydunya(request):
	return JsonResponse('Payment complet!', safe=False)
# 	transactionId = datetime.datetime.now().timestamp()
# 	data = json.loads(request.body)

# 	if request.user.is_authenticated:
# 		client = request.user.client
# 		commande, created = Commande.objects.get_or_create(client=client, complete=False)

# 	else:
# 		client, commande = guestCommande(request, data)


# 	total = float(data['form']['total'])
# 	commande.transactionId = transactionId

# 	if total == commande.get_panier_total:
# 		commande.complete = True
# 	commande.save()

# 	if commande.livraison == True:
# 		LivraisonAdresse.objects.create(
# 			client = client,
# 			commande = commande,
# 			adresse = data['livraison']['adresse'],
# 			region = data['livraison']['region'],
# 			pays = data['livraison']['pays'],
# 			telephone = data['livraison']['telephone'],
# 		)

# 	PAYDUNYA_ACCESS_TOKENS = {
# 		'PAYDUNYA-MASTER-KEY': "bTWZ1OGu-IXpy-Ml9P-e4Z3-ig09l0hEjASe",
# 		'PAYDUNYA-PRIVATE-KEY': "test_private_qbGW0GXa3pXvjqSFfdip4pmfbpR",
# 		'PAYDUNYA-TOKEN': "8F4urgDEJ3oqHAlegvPP"
# 	}
# 	paydunya.debug = True
# 	paydunya.API_keys = PAYDUNYA_ACCESS_TOKENS


	

# 	store = paydunya.Store(name='Les tuniques d\'Alima')
# 	invoice = paydunya.Invoice(store)
	
# 	store = Store(name='Les tuniques d\'Alima')

# # L'ajout d'éléments à votre facture est très basique.
# # Les paramètres attendus sont nom du produit, la quantité, le prix unitaire,
# # le prix total et une description.
# 	items = [
# 		# for article in articles:
# 			InvoiceItem(
# 				name="",
# 				quantity="",
# 				unit_price="",
# 				total_price=0,
# 				description=""
# 			),
# 		]
# 	invoice = paydunya.Invoice(store)
# 	invoice.add_items(items)


# 	invoice.description = ""



# 	invoice = paydunya.Invoice(store)
# 	invoice.add_items(items)

# 	invoice.total_amount = float(total)
# 	successful, response = invoice.create()
# 	if successful:
# 		print('response redirection : ', response)
# 	else:
# 		print('response no redirection : ', response)
# 		return JsonResponse('Payment complet!', safe=False)			







# # Configuration des informations de votre service/entreprise
	# infos = {
	# 	'name': "Les tuniques d'alima", # Seul le nom est requis
	# 	'tagline': "",
	# 	'postal_address': "Mamelles Aviation",
	# 	'phone_number': "774070749",
	# 	'website_url': "https://khadim007.herokuapp.com/",
	# 	'logo_url': ""
	# }

	# store = Store(name='Les tuniques d\'alima')
 #    # items = [
 #    #     InvoiceItem(
 #    #         name="Clavier DELL",
 #    #         quantity=2,
 #    #         unit_price="3000",
 #    #         total_price="6000",
 #    #         description="Best Keyboard of the 2015 year"
 #    #     ),
 #    #     InvoiceItem(
 #    #         name="Ordinateur Lenovo L440",
 #    #         quantity=1,
 #    #         unit_price="400000",
 #    #         total_price="400000",
 #    #         description="Powerful and slim"
 #    #     ),
 #    # ]

	# invoice = paydunya.Invoice(store)

 #    # invoice.add_items(items)

 #    # taxes are (key,value) pairs
 #    # invoice.add_taxes([("Other TAX", 5000), ("TVA (18%)", 700)])

	# invoice.add_custom_data([
 #    	("first_name", data['form']['prenom']),
 #    	("last_name", data['form']['nom']),
 #        # ("cart_id", 97628),
 #        # ("coupon", "NOEL"),
	# ])


	# invoice.callback_url = "http://www.ma-super-boutique.com/fichier_de_reception_des_données_de_facturation"


 #    # # you can also pass the items, taxes, custom to the `create` method
	# successful, response = invoice.create()
	# if successful:
	# 	do_something_with_resp(response)
	# 	print('successful')

 #    # # confirm invoice
 #    # invoice.confirm('YOUR_INVOICE_TOKEN')


 #    # # PSR
 #    # opr_data = {
 #    #     'account_alias': data['livraison']['telephone'],
 #    #     'description': 'Hello ',
 #    #     'total_amount': total
 #    # }
 #    # store = paydunya.Store(name='Les tuniques d\'alima')
 #    # opr = paydunya.OPR(opr_data, store)
 #    # # You can also pass the data to the `create` function
 #    # successful, response = opr.create()
 #    # if successful:
 #    #    do_something_with_response(response)
 #    # status, _ = opr.charge({
 #    #     'token': token,
 #    #     'confirm_token': user_submitted_token
 #    # })

 #    # # Direct Pay
 #    # account_alias =  "EMAIL_OU_NUMERO_DU_CLIENT_PAYDUNYA"
 #    # amount =  6500
 #    # # toggle debug switch to True
 #    # direct_pay = paydunya.DirectPay(account_alias, amount)
 #    # status, response = direct_pay.process()