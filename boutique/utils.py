import json
from . models import *

def cookiePanier(request):
	try:
		panier = json.loads(request.COOKIES['panier'])
	except:
		panier = {}
	print('panier', panier)
	articles = []
	commande = {"get_panier_articles":0, "get_panier_total": 0, "livraison":False}
	panierArticles = commande['get_panier_articles']

	for i in panier:
		try:
			panierArticles += panier[i]['quantite']

			produit = Produit.objects.get(id=i)
			total = (produit.prix * panier[i]['quantite'])

			commande['get_panier_total'] += total
			commande['get_panier_articles'] += panier[i]['quantite']

			article = {
				'produit':{
					'id':produit.id,
					'nom':produit.nom,
					'prix':produit.prix,
					'imageURL':produit.imageURL
					},
				'quantite':panier[i]['quantite'],
				'get_total':total,
				}
			articles.append(article)

			if produit.digital == False:
				commande['livraison'] = True
		except:
			pass
	return{'panierArticles':panierArticles, 'commande':commande, 'articles':articles}


def panierData(request):
	if request.user.is_authenticated:
		client = request.user.client
		commande, created = Commande.objects.get_or_create(client = client, complete = False)
		articles = commande.commandearticle_set.all()
		panierArticles = commande.get_panier_articles
	else:
		cookieData = cookiePanier(request)
		panierArticles = cookieData['panierArticles']
		commande = cookieData['commande']
		articles = cookieData['articles']
	return{'panierArticles':panierArticles, 'commande':commande, 'articles':articles}


def guestCommande(request , data):
	print('L\'utilisateur ne s\'est pas authentifié ...')

	print('COOKIES:', request.COOKIES)
	nom = data['form']['nom']
	email = data['form']['email']

	cookieData = cookiePanier(request)
	articles = cookieData['articles']

	client, created = Client.objects.get_or_create(
		email = email,
		)
	client.nom = nom
	client.save()

	commande = Commande.objects.create(
		client = client,
		complete = False,
		)

	for article in articles:
		produit = Produit.objects.get(id=article['produit']['id'])

		commandeArticle = CommandeArticle.objects.create(
			produit =produit,
			commande = commande,
			quantite = article['quantite'],
			)
	return client, commande

