from django.urls import path

from . import views

urlpatterns = [
	#url('^$', vue.accueil),
	path('', views.accueil, name="accueil"),
	path('tunique/', views.tunique, name="tunique"),
    path('accessoirs/', views.accessoirs, name="accessoirs"),
    path('panier/', views.panier, name="panier"),
    path('acheter/', views.acheter, name="acheter"),
    path('boss/', views.boss, name="boss"),
    path('update_article/', views.updateArticle, name="update_article"),
    path('process_commande/', views.processCommande, name="process_commande"),
    path('process_paydunya/', views.processPaydunya, name="process_paydunya"),

]
