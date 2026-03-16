# Context Engineering Workshop avec GitHub Copilot

Ce repository est un support de workshop pour apprendre le **Context Engineering** et pratiquer les techniques avancées de travail avec les LLM via GitHub Copilot.

## 🎯 Objectif

Pratiquer le **Context Engineering** en manipulant un dataset massif de tâches (~10 000 entrées). Vous apprendrez à gérer les limites de contexte des LLM, à implémenter des stratégies de chunking et de summarisation, et à utiliser efficacement GitHub Copilot pour accélérer votre développement.

## Prérequis

- GitHub Copilot activé dans VS Code
- Python 3.x installé
- Connaissances de base en Python et manipulation de fichiers JSON

## 📖 Contexte

Tu es développeur au sein de **TaskFlow**, une startup qui conçoit une plateforme collaborative de gestion de tâches pour équipes projets. La plateforme accumule des milliers de tâches issues de différents domaines (infrastructure, architecture, organisation). Pour piloter la roadmap, l'équipe a besoin d'analyser ce volume de données — mais le dataset est trop volumineux pour être simplement envoyé à un LLM.

En tant que développeur, tu vas expérimenter les limites des LLM face à de larges contextes, puis apprendre à les dépasser grâce aux techniques de Context Engineering.

### 🔌 API Endpoints

L'API existante fournit des endpoints pour la gestion des tâches :

- **GET /tasks** : Récupérer une liste de tâches.
- **POST /tasks** : Créer une nouvelle tâche.
- **GET /tasks/{id}** : Récupérer une tâche spécifique par ID.
- **PUT /tasks/{id}** : Mettre à jour une tâche spécifique par ID.
- **DELETE /tasks/{id}** : Supprimer une tâche spécifique par ID.

## 🧠 Concepts Clés

| Concept | Description |
|---|---|
| **Fenêtre de contexte** | Limite en tokens que le LLM peut traiter en une seule requête (4K–200K tokens) |
| **Chunking** | Découpage du dataset en sous-ensembles traitables indépendamment |
| **Summarisation** | Réduction intelligente d'un dataset en gardant l'information essentielle |
| **Lost in the Middle** | Phénomène où le LLM perd en précision sur les données situées au milieu du contexte |
| **Filtrage** | Extraction des seules métadonnées nécessaires avant d'envoyer au LLM |

### Déroulement

Lis attentivement chaque tâche (fichiers `TASK X - ...md`) dans l'ordre :

1. Suis les instructions **HOW** qui guident l'utilisation des fonctionnalités Copilot
2. Valide les critères d'acceptation avant de passer à la tâche suivante
3. Expérimente : n'hésite pas à essayer différentes formulations de prompts

