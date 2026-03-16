
# Requêtage de Large Contexte avec Chunking

En tant que développeur, je souhaite requêter efficacement un dataset massif (~10k tâches) qui dépasse les limites de contexte des LLM, en expérimentant d'abord les problèmes puis en appliquant des stratégies de chunking.

## WHY

Lorsqu'on travaille avec des datasets volumineux, les LLM rencontrent deux problèmes majeurs :

1. **Dépassement de contexte** : Les modèles moins puissants (4K-8K tokens) ne peuvent pas traiter le fichier entier
2. **Perte d'attention** : Même les modèles avec large contexte (100K+ tokens) perdent en précision sur les données au milieu ("Lost in the Middle")

**Objectif pédagogique** : Constater ces limitations par l'expérimentation, puis apprendre à les résoudre avec le chunking stratégique.

## WHAT

Expérimenter les limitations des LLM puis implémenter une solution robuste :

- **Phase 1 (5 min)** : Constater l'échec avec approche naïve
- **Phase 2 (5 min)** : Comprendre pourquoi ça échoue (logs, contexte)
- **Phase 3 (10 min)** : Implémenter le chunking et vérifier les résultats

**Exemple de requête** : Trouver toutes les tâches d'un type spécifique (ex: "infrastructure", "architecture")

## HOW

### Étape 1 : Expérimenter l'Échec

1. **Utiliser un modèle limité** (GPT-4o-mini ou Sonnet) en mode **Ask Copilot**
2. **Requêter directement** le fichier de fixtures :

(titre à ajuster en fonction de vos données)

```
From the fixtures file, find all tasks about Performance Optimization
and list their titles and estimated costs.
```

3. **Observer le comportement** :
   - Erreurs de contexte ?
   - Résultats incomplets ?
   - Hallucinations ?

4. **Consulter les logs Copilot** (Debug View) :
   - Quelle taille de contexte est envoyée ?
   - Y a-t-il troncature ?

### Étape 2 : Tester avec Modèle Puissant

1. **Basculer vers un modèle avec large contexte** (Claude Sonnet 3.5 ou GPT-4)
2. **Relancer la même requête**
3. **Comparer les résultats** :
   - Plus fiable ?
   - Toujours des données manquantes ?
   - Temps de réponse ?

**Constat attendu** : Même les grands modèles perdent en précision sur les datasets massifs.

### Étape 3 : Implémenter le Chunking

**Stratégie recommandée** : Fixed-size chunking

1. **Demander à l'IA de créer un script de chunking** :

```
Create a Python script that:
1. Loads the fixtures from fixtures_dump.jsonl
2. Chunks the data into batches of 500 tasks

For each chunk, query for relevant tasks
Aggregates results
Export to a results.json file
```

2. **Exécuter et vérifier** :
   - Tous les résultats sont-ils trouvés ?
   - Performance acceptable ?

### Points d'Attention

- **Taille des chunks** : Trouver l'équilibre entre performance et contexte

## RÉSULTATS ATTENDUS

✅ Compréhension concrète des limites de contexte  
✅ Script de chunking fonctionnel 
✅ Résultats fiables et complets 
✅ Bases pour TASK 3 (summarization)

## RESSOURCES

- [Chunking Strategies (Pinecone)](https://www.pinecone.io/learn/chunking-strategies/)
- [Lost in the Middle Paper](https://arxiv.org/abs/2307.03172)
- [Contextual Retrieval (Anthropic)](https://www.anthropic.com/news/contextual-retrieval)
- [Token Calculator](https://token-calculator.net/)
