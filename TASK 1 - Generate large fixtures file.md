# Génération de Fixtures Massives avec GenAI

En tant que développeur, je souhaite générer un dataset massif de fixtures (~10k tâches) dépassant les limites de
contexte des LLM, afin de préparer des exercices sur le Context Engineering.

## WHY

Le **Context Engineering** est une compétence essentielle pour travailler efficacement avec les LLM. Les modèles ont des
limites de contexte (4K-100K tokens) et ne peuvent pas traiter des inputs entiers en une seule fois. 

Pour former les développeurs à ces techniques (chunking, summarization, filtering), nous avons besoin d'un dataset
**volontairement trop grand** pour tenir dans une fenêtre de contexte. L'objectif : forcer l'utilisation de stratégies
d'optimisation.

**Défi technique** : Générer 10 000+ fixtures réalistes avec des descriptions détaillées sans écrire manuellement chaque tâche.

## WHAT

Créer un dataset de fixtures massif structuré en plusieurs batches :

- **Volume** : ~10 000~+ tâches générées dynamiquement
- **Réalisme** : Descriptions détaillées avec métriques, SLA, coûts
- **Variété** : Différents domaines (infrastructure, architecture, organisation)
- **Taille** : Dépasse les contextes LLM standards

## HOW

### Stratégies de Génération

1. **Templates dynamiques** : Utiliser des combinaisons de listes pour générer du contenu varié
2. **Batches multiples** : Diviser en plusieurs fichiers pour organisation
3. **Appels multiples** : Construire les fixtures par ajouts successifs

- prompte l'IA pour t'aider a générer ce fichier (exemple de prompt en dessous si besoin)
- si besoin (très probable), aide l'IA à corriger son travail jusqu'à ce que cela fonctionne
- génére un fichier *.jsonl pour pouvoir continuer
- regarder les logs de Copilot avec debug view. Qu'est-ce qui se passe avec le contexte ?


**Example de prompt :**
```
I want to generate fixtures for tasks. Use the Task model from task_flow_api/model.py 
and generate fixture files in tests/fixtures/ directory.

I want the fixtures file to be very big, the objective is to test Context Engineering 
practices on it, so it has to be bigger than an LLM context window (>50K tokens).

Use multiple calls to append necessary data.
```

## RESSOURCES

- [What are tokens and how to count them?](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
- [Token Counting](https://token-calculator.net/)
- [Context Engineering Guide](https://www.promptingguide.ai/guides/context-engineering-guide)