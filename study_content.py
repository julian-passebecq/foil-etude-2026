from __future__ import annotations

PAGE_GUIDE = [
    {
        "pdf_page": 1,
        "article_page": "61",
        "title": "Question de recherche et résultat annoncé",
        "summary": (
            "Le résumé pose directement la question : peut-on améliorer l'extraction d'énergie d'un foil oscillant "
            "en modifiant la trajectoire de tangage plutôt qu'en conservant une sinusoïde ? Les auteurs gardent le "
            "pilonnement sinusoïdal et remplacent le tangage par un profil progressivement plus trapézoïdal, piloté "
            "par le paramètre β. Ils annoncent une exploration de β=1 à 4, de St=0,05 à 0,5, de α₀=10° et 20° et "
            "de h₀/c=0,5 et 1. Le résultat fort annoncé dès cette page est qu'un profil correctement choisi peut "
            "augmenter jusqu'à 63 % le coefficient de puissance de sortie et jusqu'à 50 % le rendement total par "
            "rapport au cas sinusoïdal β=1."
        ),
        "important": [
            "Le papier ne teste pas une nouvelle forme de foil : il teste surtout une nouvelle loi temporelle de mouvement.",
            "β=1 correspond au cas sinusoïdal de référence ; β croissant rend le tangage plus carré/trapézoïdal.",
            "Les gains annoncés sont des maxima dans le domaine numérique étudié, pas des gains universels.",
            "L'introduction replace le concept dans la récupération d'énergie par mouvements oscillants inspirés du vivant.",
        ],
        "figures": ["Fig. 1 — schéma générique d'un dispositif d'extraction d'énergie par foil oscillant (suite p. 2)."],
        "equations_tables": ["Résumé : domaine paramétrique et gains maxima annoncés."],
        "question": "Avant de lire la suite : quels paramètres sont réellement optimisés — géométrie du foil ou trajectoire de mouvement ?",
    },
    {
        "pdf_page": 2,
        "article_page": "62",
        "title": "État de l'art et motivation du tangage non sinusoïdal",
        "summary": (
            "Cette page construit la justification scientifique. Les auteurs rappellent plusieurs résultats antérieurs sur "
            "les foils oscillants en extraction d'énergie : Davids rapporte environ 30 % d'efficacité dans un cas optimisé, "
            "Kinsey et Dumas jusqu'à 34 %, et Simpson et al. jusqu'à 43 % pour un NACA0012 avec St=0,4, angle d'attaque "
            "maximum d'environ 34,37° et un déphasage de 90° entre tangage et pilonnement. Les auteurs insistent ensuite "
            "sur une limite importante de nombreux travaux : le mouvement est prescrit, donc la dynamique réelle de la "
            "machine n'est pas couplée au fluide. Enfin, ils expliquent leur idée : des travaux antérieurs en propulsion "
            "montrent qu'un profil non sinusoïdal peut améliorer les performances, en particulier lorsqu'on modifie le "
            "tangage plutôt que le pilonnement."
        ),
        "important": [
            "Les rendements cités viennent d'études différentes et ne sont pas directement comparables entre eux.",
            "Le déphasage de 90° apparaît déjà comme une configuration importante dans la littérature citée.",
            "Le papier reconnaît explicitement la différence entre puissance hydrodynamique et puissance nette d'un système réel.",
            "La motivation principale vient d'observations précédentes sur la propulsion : modifier le tangage semble plus prometteur que modifier le pilonnement.",
        ],
        "figures": ["Fig. 1 — architecture conceptuelle avec élément d'accumulation/stockage non modélisé."],
        "equations_tables": ["Pas de nouvelle équation principale ; revue de littérature et hypothèses de modélisation."],
        "question": "Quels résultats antérieurs sont seulement du contexte, et lesquels définissent réellement la méthode utilisée ici ?",
    },
    {
        "pdf_page": 3,
        "article_page": "63",
        "title": "Méthode CFD et définition du mouvement",
        "summary": (
            "La méthode numérique est introduite ici. Les auteurs résolvent les équations de Navier-Stokes instationnaires "
            "compressibles à faible nombre de Mach avec une méthode volumes finis, dissipation artificielle d'ordre 2/4 et "
            "dual time stepping. Le calcul est réalisé à Re=10⁴ en régime laminaire. Le nombre de Mach amont est fixé à "
            "0,05 et les auteurs surveillent que le Mach local reste inférieur à 0,3 afin de rester dans un régime "
            "effectivement incompressible. La cinématique est ensuite définie : le pilonnement h(t) reste sinusoïdal, tandis "
            "que le tangage θ(t) suit une loi par morceaux contrôlée par β. Les Fig. 2 et 3 montrent directement comment "
            "β modifie la forme du tangage et, par conséquence, l'angle d'attaque effectif."
        ),
        "important": [
            "Re=10⁴ : le domaine étudié est un régime de Reynolds relativement faible et laminaire.",
            "Ma∞=0,05 : le solveur est compressible, mais utilisé de façon à reproduire un écoulement quasi incompressible.",
            "Le pilonnement est toujours sinusoïdal ; seule la loi de tangage est modifiée.",
            "La Fig. 3 montre que le pic d'angle d'attaque effectif change fortement avec β même si α₀ nominal est fixé.",
        ],
        "figures": [
            "Fig. 2 — h(t) et θ(t) sur un cycle pour plusieurs β.",
            "Fig. 3 — αeff(t) sur un cycle pour plusieurs β.",
        ],
        "equations_tables": [
            "Eq. (1)-(3) — équations de conservation et énergie totale.",
            "Eq. (4) — pilonnement h(t)=h₀ sin(ωt).",
            "Eq. (5) — loi de tangage par morceaux contrôlée par β.",
        ],
        "question": "Quand β change, est-ce que l'on change seulement la forme du mouvement ou aussi l'angle d'attaque réellement subi par le foil ?",
    },
    {
        "pdf_page": 4,
        "article_page": "64",
        "title": "Interprétation de β, angle d'attaque effectif et premières courbes de puissance",
        "summary": (
            "Les auteurs expliquent pourquoi la non-sinusoïdalité est appliquée au tangage. Dans leurs travaux antérieurs "
            "sur la propulsion, cette modification apportait davantage de bénéfice que de modifier le pilonnement. Pour β=1, "
            "le tangage est sinusoïdal et retardé de 90° par rapport au pilonnement. Lorsque β augmente, le foil passe plus "
            "de temps près des angles extrêmes ±θ₀ et les transitions deviennent plus rapides. La page définit ensuite "
            "l'angle d'attaque effectif αeff comme la somme du tangage et de l'angle induit par le pilonnement. Elle montre "
            "aussi la validation du code contre Jones et Platzer et présente la Fig. 5, première vue synthétique de C̄op en "
            "fonction de St pour différentes valeurs de β."
        ),
        "important": [
            "β n'est pas une amplitude : c'est un paramètre de forme temporelle.",
            "β=1 implique un déphasage de 90° entre tangage et pilonnement.",
            "Plus β augmente, plus les plateaux à ±θ₀ s'allongent et plus les inversions sont rapides.",
            "La Fig. 5 est centrale : elle montre que l'effet de β dépend fortement de St, h₀/c et α₀.",
        ],
        "figures": [
            "Fig. 4 — validation de l'efficacité calculée par comparaison avec Jones & Platzer.",
            "Fig. 5 — C̄op moyen en fonction de St pour β=1, 1,25, 1,5, 2 et 4.",
        ],
        "equations_tables": [
            "Eq. (6)-(7) — définition de αeff(t).",
        ],
        "question": "Pourquoi un profil plus carré pourrait-il augmenter la puissance à certains St mais la dégrader à d'autres ?",
    },
    {
        "pdf_page": 5,
        "article_page": "65",
        "title": "Définition de la puissance, du coefficient C̄op et du rendement",
        "summary": (
            "Cette page donne les équations qui transforment les forces hydrodynamiques en puissance. L'angle d'attaque "
            "nominal α₀ est défini à partir de la vitesse de pilonnement et de θ₀. La puissance instantanée est la somme de "
            "deux termes : Y·dh/dt, lié à la force transverse et au pilonnement, et M·dθ/dt, lié au moment et à la vitesse "
            "angulaire de tangage. Le coefficient de puissance C_op est ensuite normalisé par le flux cinétique de référence "
            "et décomposé en Cp1 et Cp2. La Table 1 donne les maxima de C̄op pour β=1 : 0,14 ; 0,28 ; 0,36 ; 0,73 selon "
            "h₀/c et α₀. La Fig. 6 présente le rendement total en fonction de St."
        ),
        "important": [
            "La puissance n'est pas seulement liée à la portance : le moment de tangage peut aider ou pénaliser.",
            "Cp1 correspond au terme C_L·dh/dt ; Cp2 au terme C_M·dθ/dt.",
            "La Table 1 fournit la référence sinusoïdale nécessaire pour interpréter les gains ultérieurs.",
            "À paramètres cinématiques plus élevés, les maxima de C̄op de référence augmentent fortement.",
        ],
        "figures": ["Fig. 6 — rendement total ηT en fonction de St pour plusieurs β."],
        "equations_tables": [
            "Eq. (8) — angle d'attaque nominal α₀.",
            "Eq. (9a)-(9b) — puissance instantanée et puissance moyenne.",
            "Eq. (10)-(14) — C_op, C_L, C_M et coefficient moyen.",
            "Table 1 — maxima de C̄op pour β=1.",
        ],
        "question": "Quelle part de la puissance vient du déplacement vertical et quelle part vient du tangage ?",
    },
    {
        "pdf_page": 6,
        "article_page": "66",
        "title": "Rendement total, validation numérique et synthèse de l'effet de β",
        "summary": (
            "La page complète la décomposition de puissance et définit le rendement total ηT à partir de C̄op et de la "
            "surface balayée A=2h₀. Elle décrit ensuite la validation numérique : domaine en maillage C s'étendant jusqu'à "
            "20 cordes, maillages 193×33, 385×65 et 513×129, le maillage 385×65 étant retenu pour la plupart des calculs. "
            "Les solutions Euler sont proches de la méthode de panneaux de Jones & Platzer, tandis que les résultats laminaires "
            "sont plus faibles du fait des effets visqueux. La Fig. 7 et les Tables 2-3 résument ensuite l'effet de β sur les "
            "maxima de puissance, le rendement et le St critique."
        ),
        "important": [
            "Le papier réalise bien un contrôle de dépendance au maillage, même si les détails ne sont pas reproduits.",
            "Le maillage 385×65 est le compromis principal ; 513×129 sert aux structures tourbillonnaires détaillées.",
            "La validation montre une transition de consommation à extraction d'énergie autour d'une amplitude de tangage donnée dans le cas de référence.",
            "Les Tables 2-3 sont les chiffres synthétiques les plus utiles pour comparer β=1 et β>1.",
        ],
        "figures": ["Fig. 7 — maxima de C̄op et de ηT en fonction de β."],
        "equations_tables": [
            "Eq. (15) — décomposition intégrée de C̄op en Cp1 et Cp2.",
            "Eq. (16) — rendement total ηT.",
            "Tables 2-3 — ratios de puissance/rendement et de Stc par rapport à β=1.",
        ],
        "question": "La hausse de performance vient-elle d'un meilleur pic uniquement, ou aussi d'une plage de St plus large ?",
    },
    {
        "pdf_page": 7,
        "article_page": "67",
        "title": "Résultat global : un optimum, pas une amélioration monotone",
        "summary": (
            "La section 3.2 analyse systématiquement la puissance et le rendement. Pour toutes les configurations étudiées, "
            "C̄op augmente avec St jusqu'à un St critique Stc puis décroît. À β et α₀ fixés, une amplitude h₀/c plus élevée "
            "donne généralement un niveau de puissance plus important et repousse Stc. Par rapport à β=1, les cas β=1,25, "
            "1,5 et 2 améliorent la puissance sur une plage significative de St, surtout pour h₀/c=1. β=4 ne procure un "
            "avantage qu'à très faible St et devient ensuite inférieur au cas sinusoïdal. La page introduit aussi la Fig. 8 "
            "et la Table 4, qui décomposent la puissance en Cp1 et Cp2."
        ),
        "important": [
            "Le comportement C̄op(St) possède un optimum en St pour chaque trajectoire.",
            "β=1,25 et 1,5 couvrent la plus large plage de St à forte puissance dans les cas étudiés.",
            "β=4 illustre la limite de l'idée : rendre le tangage toujours plus carré finit par dégrader le bilan.",
            "La Table 4 prépare l'explication physique en séparant la contribution de portance et la contribution de moment.",
        ],
        "figures": ["Fig. 8 — C_op instantané, Cp1 et Cp2 sur un cycle pour β=1, 1,5, 2 et 4."],
        "equations_tables": ["Table 4 — C̄op, C̄p1 et C̄p2 à St=0,35 et α₀=10°."],
        "question": "Pourquoi β=1,5 est-il meilleur que β=1 alors que β=4 devient mauvais ?",
    },
    {
        "pdf_page": 8,
        "article_page": "68",
        "title": "Critères quantitatifs et décomposition des signes",
        "summary": (
            "Les auteurs formalisent ici les ratios utilisés pour mesurer l'amélioration ou la dégradation par rapport à "
            "β=1 : rapports des maxima de C̄op et ηT, et variation du St critique. La Fig. 9 montre ensuite, pour β=1, 1,5 "
            "et 4, quatre grandeurs instantanées : C_L, dh/dt, C_M et dθ/dt. Cette figure est essentielle pour comprendre "
            "les signes : la puissance issue du pilonnement dépend du produit C_L·dh/dt, tandis que la puissance associée "
            "au tangage dépend du produit C_M·dθ/dt. La suite du papier va montrer que ces deux termes évoluent de façon "
            "très différente lorsque β augmente."
        ),
        "important": [
            "Les ratios des Tables 2-3 ne sont pas des moyennes globales : ils comparent des maxima ou minima spécifiques.",
            "La Fig. 9 relie directement la cinématique aux forces et moments.",
            "Le signe du produit est aussi important que l'amplitude des coefficients.",
            "La durée pendant laquelle deux grandeurs gardent le même signe devient un mécanisme clé de performance.",
        ],
        "figures": ["Fig. 9 — C_L, dh/dt, C_M et dθ/dt pour β=1, 1,5 et 4."],
        "equations_tables": ["Rappel des ratios définis à partir des Tables 2-3."],
        "question": "Sur un cycle, faut-il maximiser les forces, ou surtout faire coïncider leur signe avec la vitesse correspondante ?",
    },
    {
        "pdf_page": 9,
        "article_page": "69",
        "title": "Chiffres clés et début de l'explication physique",
        "summary": (
            "Cette page donne les chiffres les plus mémorables. Le meilleur gain de puissance atteint 63 % par rapport à "
            "β=1 pour β=1,5, h₀/c=1 et α₀=10°. À l'inverse, β=4 peut réduire le maximum de puissance de 46 % pour h₀/c=1 "
            "et α₀=20°. Le rendement peut gagner jusqu'à 50 % avec β=1,5 et perdre jusqu'à 48 % avec β=4. Pour Stc, "
            "l'extension maximale atteint 1,347 fois la référence avec β=1,25 ; β=4 peut ramener Stc à 43-66 % de la "
            "valeur de référence. La section 3.3 démarre ensuite l'analyse physique et la Fig. 10 montre les champs de "
            "vorticité pour β=1."
        ),
        "important": [
            "+63 % de C̄op maximal : meilleur cas cité dans le papier.",
            "+50 % de rendement maximal : meilleur cas cité pour ηT.",
            "β=1,25 maximise l'extension de Stc dans les cas étudiés.",
            "Les auteurs sélectionnent β=1,5 comme cas favorable et β=4 comme cas défavorable pour expliquer le mécanisme.",
        ],
        "figures": ["Fig. 10 — vorticité instantanée sur un demi-cycle pour β=1."],
        "equations_tables": ["Synthèse chiffrée des Tables 2-3."],
        "question": "Le meilleur β pour la puissance maximale est-il forcément le même que pour la largeur de la plage de fonctionnement ?",
    },
    {
        "pdf_page": 10,
        "article_page": "70",
        "title": "Pourquoi Cp1 augmente mais Cp2 peut annuler le gain",
        "summary": (
            "La décomposition de la Fig. 8 est interprétée en détail. Cp1, lié à C_L·dh/dt, est généralement positif sur "
            "une grande partie du cycle ; Cp2, lié à C_M·dθ/dt, est généralement négatif. À β=1,5, les pics positifs de Cp1 "
            "augmentent et la durée de contribution positive s'étend, notamment pendant les plateaux de tangage. Cp2 devient "
            "aussi plus négatif autour des inversions, mais pas suffisamment pour annuler le gain de Cp1. Lorsque β passe à "
            "2 puis 4, la contribution négative de Cp2 devient de plus en plus importante et peut finir par dominer le bilan "
            "moyen. La Fig. 11 montre les vortex correspondants pour β=1,5."
        ),
        "important": [
            "Cp1 est le moteur positif principal dans le cas favorable.",
            "Cp2 représente un coût hydrodynamique lié au moment de tangage.",
            "Le bénéfice de β=1,5 vient d'un compromis temporel, pas seulement de forces plus élevées.",
            "À β=4, le terme négatif de moment devient suffisamment grand pour rendre le bilan défavorable.",
        ],
        "figures": ["Fig. 11 — vorticité instantanée pour β=1,5."],
        "equations_tables": ["Interprétation détaillée de la Table 4 et de la Fig. 8."],
        "question": "Quelle modification augmente plus vite lorsque β devient grand : la contribution positive de portance ou le coût du moment ?",
    },
    {
        "pdf_page": 11,
        "article_page": "71",
        "title": "Découpage du cycle A-E et logique des signes",
        "summary": (
            "Les auteurs analysent plus finement C_L et dh/dt en divisant le cycle en cinq intervalles A à E pour β=1,5. "
            "Dans A, C et E, C_L et dh/dt ont le même signe : leur produit est donc positif et contribue à l'extraction "
            "d'énergie. Dans B et D, les signes sont opposés et Cp1 devient négatif. Lorsque β augmente, B et D deviennent "
            "plus courts, ce qui réduit la part négative de Cp1. Cette analyse explique pourquoi un tangage aplati peut "
            "améliorer la contribution de portance. La Fig. 12 montre en parallèle les vortex pour β=4, cas où la "
            "cinématique devient beaucoup plus brutale."
        ),
        "important": [
            "A, C, E : contribution Cp1 positive.",
            "B, D : contribution Cp1 négative.",
            "L'amélioration de Cp1 vient en partie d'un changement de durée des intervalles favorables/défavorables.",
            "Ce mécanisme favorable n'est toutefois pas suffisant à β élevé, car Cp2 évolue en sens contraire.",
        ],
        "figures": ["Fig. 12 — vorticité instantanée pour β=4."],
        "equations_tables": ["Lecture qualitative de Fig. 9 via les intervalles A-E."],
        "question": "La performance dépend-elle davantage de la valeur maximale de C_L ou du temps passé dans les combinaisons de signes favorables ?",
    },
    {
        "pdf_page": 12,
        "article_page": "72",
        "title": "Pourquoi le moment de tangage devient pénalisant à grand β",
        "summary": (
            "La page analyse C_M et dθ/dt. Contrairement au cas C_L·dh/dt, C_M et dθ/dt ont presque toujours des signes "
            "opposés lorsque le foil est en rotation, ce qui rend Cp2 négatif. Quand θ reste bloqué à ±θ₀, dθ/dt=0 et le "
            "moment ne contribue pas à la puissance. Mais lorsque β augmente, les phases de transition deviennent plus "
            "courtes et surtout beaucoup plus rapides : les pics de dθ/dt augmentent fortement, tout comme les amplitudes "
            "de C_M. À β suffisamment élevé, le produit négatif C_M·dθ/dt dépasse le bénéfice de C_L·dh/dt. La section "
            "3.3.2 introduit ensuite les champs d'écoulement et la Fig. 13 présente la pression de paroi pour β=1."
        ),
        "important": [
            "Le coût de tangage n'est actif que lorsque dθ/dt≠0, mais il peut devenir très intense pendant ces intervalles courts.",
            "Augmenter β concentre la rotation dans des transitions plus rapides.",
            "Les pics de dθ/dt croissent alors fortement ; c'est la cause mécanique centrale de la dégradation à grand β.",
            "La Fig. 13 commence la chaîne explicative vortex → pression → forces/moments → puissance.",
        ],
        "figures": ["Fig. 13 — pression instantanée sur les parois supérieure et inférieure pour β=1."],
        "equations_tables": ["Rappel : Cp2 ∝ C_M·dθ/dt."],
        "question": "Un mouvement plus proche d'un créneau est-il réaliste si l'on tient compte des vitesses et accélérations de commande nécessaires ?",
    },
    {
        "pdf_page": 13,
        "article_page": "73",
        "title": "Vortex de bord d'attaque, pression de surface et contribution de portance",
        "summary": (
            "Les auteurs suivent l'évolution du vortex de bord d'attaque (LEV) sur un demi-cycle. Il commence à se former "
            "autour de t=0, grandit et atteint sa plus forte intensité parmi les instantanés présentés vers t=T/4, puis "
            "se déplace le long du profil avant d'être éjecté dans le sillage. Cette évolution crée des minima locaux de "
            "pression sur la surface. Les distributions de pression sont fortement liées à l'angle d'attaque effectif et "
            "déterminent directement C_L et C_M. Sur certaines phases, une portance négative est associée à une vitesse de "
            "pilonnement également négative, donc le produit C_L·dh/dt reste positif : une force dirigée vers le bas peut "
            "ainsi contribuer positivement à l'extraction si le mouvement est lui aussi dirigé vers le bas."
        ),
        "important": [
            "Le LEV est un intermédiaire physique important, mais le papier ne dit pas simplement qu'un vortex plus fort est toujours meilleur.",
            "La pression de surface est le lien direct entre structure d'écoulement et forces hydrodynamiques.",
            "Le signe de la puissance dépend de l'alignement force-vitesse, pas du signe absolu de la portance.",
            "La moitié suivante du cycle est inverse-symétrique dans le modèle étudié.",
        ],
        "figures": ["Fig. 14 — pression de paroi pour β=1,5."],
        "equations_tables": ["Lien qualitatif entre αeff, pression, C_L et Cp1."],
        "question": "Comment une portance négative peut-elle malgré tout produire une puissance positive ?",
    },
    {
        "pdf_page": 14,
        "article_page": "74",
        "title": "Pression, moment de tangage et début des conclusions",
        "summary": (
            "La discussion se concentre sur le moment autour de l'axe de tangage placé à x=c/3. Autour des inversions, "
            "le moment aérodynamique agit en sens opposé au mouvement de tangage alors que |dθ/dt| est élevé : le produit "
            "C_M·dθ/dt devient donc fortement négatif et domine la pénalité énergétique. La Fig. 15 montre la pression pour "
            "β=4, cas où ces effets sont les plus extrêmes. La conclusion commence ensuite : pour St inférieur au St critique, "
            "un profil de tangage non sinusoïdal bien choisi peut augmenter significativement la puissance moyenne et le "
            "rendement, mais l'optimum dépend de β et des paramètres cinématiques."
        ),
        "important": [
            "L'axe à c/3 est essentiel pour interpréter le signe du moment.",
            "La pénalité Cp2 est concentrée autour des inversions rapides.",
            "Le bénéfice d'un profil aplati n'est pas universel : il existe un optimum de β.",
            "La conclusion insiste autant sur l'extension de Stc que sur l'augmentation du pic de puissance.",
        ],
        "figures": ["Fig. 15 — pression de paroi pour β=4."],
        "equations_tables": ["Début de la section 4 — conclusions."],
        "question": "La loi de mouvement optimale hydrodynamiquement resterait-elle optimale une fois ajoutés les efforts mécaniques de commande ?",
    },
    {
        "pdf_page": 15,
        "article_page": "75",
        "title": "Conclusion finale, optimum β≈1,5 et limite majeure du modèle",
        "summary": (
            "La dernière page résume le mécanisme : Cp1 augmente avec β et reste globalement positif parce que C_L et dh/dt "
            "ont souvent le même signe ; Cp2 est négatif parce que C_M et dθ/dt sont opposés pendant les rotations. Pour un "
            "β légèrement supérieur à 1, Cp1 reste dominant et la performance s'améliore. Lorsque β devient trop grand, "
            "Cp2 augmente beaucoup plus vite et finit par dominer. Dans le domaine cinématique étudié, l'optimum est autour "
            "de β=1,5. Les auteurs terminent par leur principale réserve : tangage et pilonnement sont prescrits et la réponse "
            "dynamique du dispositif aux charges instationnaires est découplée. Ils indiquent que le couplage fluide-structure "
            "est une étape suivante nécessaire."
        ),
        "important": [
            "L'optimum β≈1,5 est valable pour le domaine testé, pas comme constante universelle.",
            "Le mécanisme final est un compromis Cp1 positif / Cp2 négatif.",
            "La dynamique du mécanisme réel n'est pas simulée : le mouvement est imposé.",
            "Le papier fournit surtout une règle de conception de trajectoire à tester ensuite dans un modèle couplé et expérimental.",
        ],
        "figures": ["Fin de la conclusion puis bibliographie."],
        "equations_tables": ["Aucune nouvelle équation ; synthèse et limites."],
        "question": "Quelle serait la prochaine validation indispensable avant de transposer ce résultat à une machine réelle ?",
    },
]

PRIOR_WORK = [
    {
        "reference": "McKinney & DeLaurier",
        "reported_result": "Extraction de puissance démontrée avec mouvement tangage-pilonnement ; efficacité décrite comme comparable à une éolienne rotative.",
        "reader_note": "Résultat cité par Xiao et al. comme travail pionnier ; pas une donnée directement comparable aux cas du papier.",
    },
    {
        "reference": "Davids",
        "reported_result": "Efficacité totale rapportée jusqu'à ~30 % avec NACA0012 et combinaison optimisée amplitude/fréquence.",
        "reader_note": "Valeur issue de la littérature citée dans l'introduction.",
    },
    {
        "reference": "Kinsey & Dumas",
        "reported_result": "Efficacité maximale rapportée jusqu'à ~34 % dans leur domaine paramétrique.",
        "reader_note": "Calcul numérique cité ; conditions et définitions diffèrent de celles du présent papier.",
    },
    {
        "reference": "Simpson et al.",
        "reported_result": "Maximum hydrodynamique rapporté à ~43 % pour AR=7,9, St=0,4, angle d'attaque max ~34,37° et déphasage 90°.",
        "reader_note": "Résultat expérimental cité dans l'introduction ; utile comme contexte, non comme benchmark direct.",
    },
    {
        "reference": "Zhu & Peng",
        "reported_result": "Études couplées où le tangage est prescrit et le pilonnement répond aux charges ; extraction nette positive surtout à basse fréquence.",
        "reader_note": "Important pour comprendre la limite du mouvement entièrement prescrit.",
    },
]

METHOD_FACTS = [
    ("Profil", "NACA0012"),
    ("Type de calcul", "2D, instationnaire, visqueux"),
    ("Solveur", "Navier-Stokes compressible à faible Mach, volumes finis"),
    ("Reynolds", "Re = 10⁴"),
    ("Mach amont", "Ma∞ = 0,05"),
    ("Hypothèse d'écoulement", "Laminaire ; Mach local contrôlé < 0,3"),
    ("Domaine", "Maillage de type C jusqu'à 20 cordes dans toutes les directions"),
    ("Maillages", "193×33, 385×65, 513×129"),
    ("Maillage principal", "385×65"),
    ("Maillage vortex détaillé", "513×129"),
    ("Axe de tangage", "c/3 depuis le bord d'attaque"),
    ("β testés", "1 ; 1,25 ; 1,5 ; 2 ; 4"),
    ("h₀/c", "0,5 ; 1,0"),
    ("α₀", "10° ; 20°"),
    ("St", "0,05 à 0,5 annoncé dans le résumé ; plage détaillée dépendant du cas"),
]

EQUATION_GUIDE = [
    {
        "name": "Pilonnement",
        "equation": r"h(t)=h_0\sin(\omega t)",
        "meaning": "Le déplacement vertical reste parfaitement sinusoïdal dans toute l'étude.",
        "source": "Eq. (4), PDF p. 3",
    },
    {
        "name": "Tangage",
        "equation": "θ(t) = loi par morceaux contrôlée par β",
        "meaning": "β=1 donne une sinusoïde ; β>1 allonge les plateaux à ±θ₀ et raccourcit les transitions.",
        "source": "Eq. (5), PDF p. 3",
    },
    {
        "name": "Angle d'attaque effectif",
        "equation": r"\alpha_{eff}(t)=-\arctan\left(\frac{\dot h}{U_\infty}\right)+\theta(t)",
        "meaning": "Le foil voit à la fois l'orientation imposée par le tangage et l'angle induit par sa vitesse verticale.",
        "source": "Eq. (7), PDF p. 4",
    },
    {
        "name": "Angle nominal",
        "equation": r"\alpha_0=-\arctan\left(\frac{\omega h_0}{U_\infty}\right)+\theta_0",
        "meaning": "Paramètre fixe utilisé pour construire les cas comparés dans les figures.",
        "source": "Eq. (8), PDF p. 5",
    },
    {
        "name": "Puissance instantanée",
        "equation": r"P(t)=Y(t)\dot h(t)+M(t)\dot\theta(t)",
        "meaning": "Deux voies d'échange d'énergie : force transverse × vitesse verticale, et moment × vitesse angulaire.",
        "source": "Eq. (9a), PDF p. 5",
    },
    {
        "name": "Coefficient de puissance",
        "equation": r"C_{op}=\frac{1}{U_\infty}\left(C_L\dot h+C_M\dot\theta\right)=C_{p1}+C_{p2}",
        "meaning": "Décomposition fondamentale utilisée pour expliquer le mécanisme d'amélioration ou de dégradation.",
        "source": "Eq. (11), PDF p. 5",
    },
    {
        "name": "Rendement total",
        "equation": r"\eta_T=C_{op}\frac{c}{A},\quad A=2h_0",
        "meaning": "La puissance extraite est normalisée par la puissance disponible sur la surface balayée.",
        "source": "Eq. (16), PDF p. 6",
    },
]

INTERVAL_GUIDE = [
    ("A", "C_L et dh/dt de même signe", "Cp1 positif"),
    ("B", "C_L et dh/dt de signes opposés", "Cp1 négatif"),
    ("C", "C_L et dh/dt de même signe", "Cp1 positif"),
    ("D", "C_L et dh/dt de signes opposés", "Cp1 négatif"),
    ("E", "C_L et dh/dt de même signe", "Cp1 positif"),
]

PAPER_PDF_URL = "https://www.cfd-fsi-xiao.org/wp-content/uploads/2024/12/1-s2.0-S0960148111002576-main.pdf"

# Crop boxes measured on a 1241 x 1654 render of the source PDF.
# They are converted to normalized coordinates at runtime, so rendering can use any DPI.
_FIGURE_PIXEL_BOXES = {
    1: (2, (60, 1190, 610, 1545)),
    2: (3, (70, 110, 605, 640)),
    3: (3, (635, 110, 1170, 640)),
    4: (4, (60, 100, 600, 650)),
    5: (4, (275, 765, 980, 1540)),
    6: (5, (275, 800, 995, 1545)),
    7: (6, (70, 100, 605, 1135)),
    8: (7, (245, 110, 1010, 835)),
    9: (8, (195, 325, 1040, 1545)),
    10: (9, (235, 500, 1030, 1535)),
    11: (10, (235, 500, 1030, 1535)),
    12: (11, (235, 500, 1030, 1535)),
    13: (12, (210, 500, 1030, 1540)),
    14: (13, (210, 500, 1030, 1540)),
    15: (14, (210, 100, 1030, 1000)),
}

FIGURE_TITLES = {
    1: "Schéma d'un dispositif d'extraction d'énergie par foil oscillant",
    2: "Profils de pilonnement h(t) et de tangage θ(t)",
    3: "Angle d'attaque effectif αeff(t)",
    4: "Validation numérique contre Jones & Platzer",
    5: "Coefficient de puissance moyen C̄op en fonction de St",
    6: "Rendement total ηT en fonction de St",
    7: "Maxima de puissance et de rendement en fonction de β",
    8: "Décomposition instantanée C_op = Cp1 + Cp2",
    9: "C_L, dh/dt, C_M et dθ/dt sur un cycle",
    10: "Vorticité instantanée pour β=1",
    11: "Vorticité instantanée pour β=1,5",
    12: "Vorticité instantanée pour β=4",
    13: "Pression de paroi pour β=1",
    14: "Pression de paroi pour β=1,5",
    15: "Pression de paroi pour β=4",
}

FIGURE_CROPS = {
    fig: {
        "page": page,
        "box": tuple(value / scale for value, scale in zip(box, (1241, 1654, 1241, 1654))),
        "title": FIGURE_TITLES[fig],
    }
    for fig, (page, box) in _FIGURE_PIXEL_BOXES.items()
}

PAGE_FIGURES = {
    page: [fig for fig, meta in FIGURE_CROPS.items() if meta["page"] == page]
    for page in range(1, 16)
}
