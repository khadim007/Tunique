
var updateBtns = document.getElementsByClassName("update-panier");

for(var i=0 ; i < updateBtns.length; i++){
	updateBtns[i].addEventListener('click',function(){
		var produitId = this.dataset.produit
		var action = this.dataset.action
		console.log('produitId: ',produitId,' action: ',action)
		console.log('USER :'+user)

		if(user == 'AnonymousUser'){
			addCookieArticle(produitId, action)
		}else{
			updateClientCommande(produitId,action)
		}

	})
}


function addCookieArticle(produitId, action){
	console.log('Utilisateur non authentifié..')

	if (action == 'add'){
		if (panier[produitId] == undefined){
			panier[produitId] = {'quantite':1}
		}else{
			panier[produitId]['quantite'] += 1
		}
	}

	if (action == 'remove'){
		panier[produitId]['quantite'] -= 1

		if(panier[produitId]['quantite'] <= 0){
			console.log('remove article')
			delete panier[produitId]
		}
	}
	console.log('panier:',panier)
	document.cookie = 'panier=' + JSON.stringify(panier) + ";domain=;path=/;Secure" 
	location.reload()

}




function updateClientCommande(produitId,action){
	console.log('ok')

	var url = '/boutique\/update_article/'

	fetch(url,{
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'produitId':produitId,'action':action})
	})
	.then((response) => {
		return response.json()
	})
	.then((data) => {
		console.log('Data:',data)
		location.reload()
	});
}


