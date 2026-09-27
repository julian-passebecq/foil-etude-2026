# Foil — étude 2026 : compagnon de lecture Streamlit

Application en français pour accompagner la lecture de l'article :

> Q. Xiao, W. Liao, S. Yang, Y. Peng, *How motion trajectory affects energy extraction performance of a biomimic energy generator with an oscillating foil?*, Renewable Energy 37 (2012) 61-75. DOI: 10.1016/j.renene.2011.05.029

## Objectif

L'app ne remplace pas le papier. Elle sert de guide de lecture pour Francis :

- résumé très court et parcours par pages ;
- visualisation interactive du profil de tangage contrôlé par `β` ;
- reconstruction de `αeff` à partir des équations de l'article ;
- graphiques des valeurs exactes des Tables 1 à 4 ;
- explication du mécanisme `Cp1 + Cp2` ;
- repères pour les figures de vortex et de pression ;
- rappel explicite des limites du modèle.

Aucune courbe CFD absente des tables n'est inventée ou interpolée.

## Lancer localement

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Source des données de l'app

- Table 1 : maxima de coefficient de puissance pour `β=1`.
- Table 2 : ratios maximum/minimum de puissance et rendement pour `β>1` vs `β=1`.
- Table 3 : ratios du Strouhal critique `Stc`.
- Table 4 : décomposition moyenne `Cop = Cp1 + Cp2` à `St=0.35`, `α0=10°`.
- Équations (4), (5), (7), (8) : widget cinématique.

## Important

L'article est une étude numérique d'un foil NACA0012 à `Re=10^4`, avec mouvements prescrits. Il ne constitue pas, à lui seul, une validation d'une machine Foil'O complète ni d'un LCOE.

## Vérification

La logique scientifique est isolée dans `study_model.py` afin de pouvoir être testée sans l'interface Streamlit.

- tests numériques de l'équation de tangage et de la périodicité ;
- contrôle des quatre scénarios des Tables 1 à 3 ;
- contrôle des signes et de la cohérence d'arrondi de la Table 4 ;
- smoke test Streamlit ;
- CI : compilation Python + `pytest`.
