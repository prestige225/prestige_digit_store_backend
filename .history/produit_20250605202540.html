
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Ajouter un produit</title>
</head>
<body>

<h2>Ajouter un produit</h2>

<form id="addProductForm" enctype="multipart/form-data">
  <label>Nom du produit : </label><br />
  <input type="text" name="nom" required /><br />

  <label>Description : </label><br />
  <textarea name="description"></textarea><br />

  <label>Prix (€) : </label><br />
  <input type="number" name="prix" step="0.01" required /><br />

  <label>Stock : </label><br />
  <input type="number" name="stock" required /><br />

  <label>Image : </label><br />
  <input type="file" name="image" accept="image/*" required /><br /><br />

  <button type="submit">Ajouter</button>
</form>

<script>
document.getElementById('addProductForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);

  try {
    const response = await fetch('http://localhost:3000/api/produits', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      alert('Produit ajouté avec succès !');
      e.target.reset();
    } else {
      const error = await response.json();
      alert('Erreur : ' + (error.error || 'Erreur inconnue'));
    }
  } catch (err) {
    alert('Erreur réseau ou serveur');
  }
});
</script>

</body>
</html>
