"""
Test unitaire qui reproduit le bug:
Le champ completed ne persiste pas lors d'un PUT /tasks/{id} avec status: "ARCHIVED"

Comportement actuel : L'API retourne 200 OK mais completed reste false après rechargement.
Comportement attendu : status: "ARCHIVED" doit automatiquement passer completed: true et persister en base.
"""

import pytest
from fastapi.testclient import TestClient
from task_flow_api.main import app


def test_archived_status_should_set_completed_to_true():
    """
    Test qui reproduit le bug:
    Lorsqu'on met à jour une tâche avec status="ARCHIVED",
    le champ completed devrait être automatiquement mis à true et persister en base.
    """
    with TestClient(app) as client:
        # Étape 1: Créer une tâche initiale avec status TODO
        create_response = client.post(
            "/tasks",
            json={
                "title": "Test Task for Archive Bug",
                "description": "This task will be archived to test the bug reproduction scenario",
                "status": "TODO",
                "completed": False,
            },
        )

        assert create_response.status_code == 200
        created_task = create_response.json()
        task_id = created_task["id"]

        # Vérifier que la tâche initiale a bien completed=False
        assert created_task["completed"] is False
        assert created_task["status"] == "TODO"

        # Étape 2: Mettre à jour la tâche avec status="ARCHIVED"
        update_response = client.put(
            f"/tasks/{task_id}",
            json={
                "id": task_id,
                "title": "Test Task for Archive Bug",
                "description": "This task will be archived to test the bug reproduction scenario",
                "status": "ARCHIVED",
                "completed": False,  # On envoie false volontairement
                "created_at": created_task["created_at"],
            },
        )

        assert update_response.status_code == 200
        updated_task = update_response.json()

        # Vérifier que le status a bien été changé
        assert updated_task["status"] == "ARCHIVED"

        # BUG REPRODUIT ICI: Le champ completed devrait être True mais reste False
        # Ce test va ÉCHOUER tant que le bug n'est pas corrigé
        assert updated_task["completed"] is True, (
            "BUG: Le champ completed devrait être automatiquement mis à True "
            "lorsque le status passe à ARCHIVED"
        )

        # Étape 3: Recharger la tâche pour vérifier la persistance en base
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200
        reloaded_task = get_response.json()

        # Vérifier que completed=True a bien persisté en base de données
        assert reloaded_task["completed"] is True, (
            "BUG: Le champ completed=True ne persiste pas en base de données "
            "après la mise à jour avec status=ARCHIVED"
        )
        assert reloaded_task["status"] == "ARCHIVED"


def test_archived_status_persists_completed_true_even_if_explicitly_set():
    """
    Test supplémentaire: Même si on envoie explicitement completed=True avec status="ARCHIVED",
    cela devrait persister correctement.
    """
    with TestClient(app) as client:
        # Créer une tâche
        create_response = client.post(
            "/tasks",
            json={
                "title": "Another Test Task",
                "description": "Testing explicit completed true with archived status",
                "status": "TODO",
                "completed": False,
            },
        )

        assert create_response.status_code == 200
        task_id = create_response.json()["id"]
        created_at = create_response.json()["created_at"]

        # Mettre à jour avec ARCHIVED et completed=True explicitement
        update_response = client.put(
            f"/tasks/{task_id}",
            json={
                "id": task_id,
                "title": "Another Test Task",
                "description": "Testing explicit completed true with archived status",
                "status": "ARCHIVED",
                "completed": True,
                "created_at": created_at,
            },
        )

        assert update_response.status_code == 200

        # Recharger et vérifier
        get_response = client.get(f"/tasks/{task_id}")
        reloaded_task = get_response.json()

        assert reloaded_task["status"] == "ARCHIVED"
        assert reloaded_task["completed"] is True, (
            "Le champ completed=True devrait persister même quand envoyé explicitement"
        )


def test_archived_from_in_progress_should_set_completed():
    """
    Test: Archiver une tâche en IN_PROGRESS devrait mettre completed à True
    """
    with TestClient(app) as client:
        create_response = client.post(
            "/tasks",
            json={
                "title": "In Progress Task",
                "description": "Task to test archiving from IN_PROGRESS",
                "status": "IN_PROGRESS",
                "completed": False,
            },
        )

        task_id = create_response.json()["id"]
        created_at = create_response.json()["created_at"]

        update_response = client.put(
            f"/tasks/{task_id}",
            json={
                "id": task_id,
                "title": "In Progress Task",
                "description": "Task to test archiving from IN_PROGRESS",
                "status": "ARCHIVED",
                "completed": False,
                "created_at": created_at,
            },
        )

        assert update_response.status_code == 200
        assert update_response.json()["completed"] is True

        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.json()["completed"] is True


def test_multiple_updates_to_archived_maintains_completed():
    """
    Test: Plusieurs mises à jour successives vers ARCHIVED devraient maintenir completed=True
    """
    with TestClient(app) as client:
        create_response = client.post(
            "/tasks",
            json={
                "title": "Multiple Update Task",
                "description": "Testing multiple updates",
                "status": "TODO",
                "completed": False,
            },
        )

        task_id = create_response.json()["id"]
        created_at = create_response.json()["created_at"]

        # Première mise à jour vers ARCHIVED
        client.put(
            f"/tasks/{task_id}",
            json={
                "id": task_id,
                "title": "Multiple Update Task - Updated 1",
                "description": "Testing multiple updates",
                "status": "ARCHIVED",
                "completed": False,
                "created_at": created_at,
            },
        )

        # Deuxième mise à jour (modifier le titre mais garder ARCHIVED)
        update_response = client.put(
            f"/tasks/{task_id}",
            json={
                "id": task_id,
                "title": "Multiple Update Task - Updated 2",
                "description": "Testing multiple updates",
                "status": "ARCHIVED",
                "completed": False,
                "created_at": created_at,
            },
        )

        assert update_response.json()["completed"] is True

        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.json()["completed"] is True


def test_archived_status_with_done_status_transition():
    """
    Test: Passage de DONE à ARCHIVED devrait maintenir completed=True
    """
    with TestClient(app) as client:
        create_response = client.post(
            "/tasks",
            json={
                "title": "Done to Archived Task",
                "description": "Testing DONE to ARCHIVED transition",
                "status": "DONE",
                "completed": True,
            },
        )

        task_id = create_response.json()["id"]
        created_at = create_response.json()["created_at"]

        update_response = client.put(
            f"/tasks/{task_id}",
            json={
                "id": task_id,
                "title": "Done to Archived Task",
                "description": "Testing DONE to ARCHIVED transition",
                "status": "ARCHIVED",
                "completed": False,  # Envoyer false pour tester l'override
                "created_at": created_at,
            },
        )

        assert update_response.json()["completed"] is True

        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.json()["completed"] is True
