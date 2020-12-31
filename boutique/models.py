from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Client(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
	prenom = models.CharField(max_length = 200, null = True)
	nom = models.CharField(max_length = 200, null = True)
	email = models.EmailField(max_length = 200, null = True)

	def __str__(self):
		return self.nom
	



class Produit(models.Model):
	nom = models.CharField(max_length = 200)
	prix = models.DecimalField(max_digits=7, decimal_places=2)
	digital = models.BooleanField(default = False, null = True, blank = False)
	image = models.ImageField(null = True, blank = False)
	typee = models.CharField(max_length = 210, default = "tunique")

	def __str__(self):
		return self.nom

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ""
		return url

class Commande(models.Model):
	client = models.ForeignKey(Client, on_delete = models.SET_NULL, blank = True, null = True)
	dateCommande = models.DateTimeField(auto_now_add = True)
	complete = models.BooleanField(default = False, blank = True, null = True)
	transactionId = models.CharField(max_length = 200, null=True)

	def __str__ (self):
		return str(self.id)

	@property
	def livraison(self):
		livraison = False
		commandearticles = self.commandearticle_set.all()
		for i in commandearticles:
			if i.produit.digital == False :
				livraison = True

		return livraison
	

	@property
	def get_panier_total(self):
		comArticle = self.commandearticle_set.all()
		total = sum([item.get_total for item in comArticle])
		return total

	def get_panier_articles(self):
		comArticle = self.commandearticle_set.all()
		total = sum([item.quantite for item in comArticle])
		return total
	

class CommandeArticle(models.Model):
	produit = models.ForeignKey(Produit, on_delete = models.SET_NULL, blank = True, null = True)
	commande = models.ForeignKey(Commande, on_delete = models.SET_NULL, blank = True, null = True)
	quantite = models.IntegerField(default = 0, blank = True, null = True)
	dateAjouter = models.DateTimeField(auto_now_add = True)

	@property
	def get_total(self):
		total = self.produit.prix * self.quantite
		return total
	

class LivraisonAdresse(models.Model):
	client = models.ForeignKey(Client, on_delete = models.SET_NULL, blank = True, null = True)
	commande = models.ForeignKey(Commande, on_delete = models.SET_NULL, blank = True, null = True)
	adresse = models.CharField(max_length = 200, null = True)
	region = models.CharField(max_length = 200, null = True)
	pays = models.CharField(max_length = 200, null = True)
	telephone = models.CharField(max_length = 200, null = True)
	dateAjouter = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.adresse

