# scrapping
scrapping pour la nuit de l'info 2021

## Siphonnage

Pour obtenir toutes les données du site : 
```
wget --recursive --no-clobber --page-requisites --html-extension --convert-links --domains sauveteurdudunkerquois.fr --no-parent https://sauveteurdudunkerquois.fr
```

Nous avons ensuite utiliser les fichiers json de `/wp-json/wp/v2/pages/`.
