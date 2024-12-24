import pytest
import logging
logging.basicConfig(level=logging.DEBUG)

@pytest.mark.timeout(10)
def test_add_flashcard(test_client):
    logging.debug("Start tests")
    # Add a category first (required for adding a flashcard)
    if not Category.query.filter_by(name='Python').first():
        test_client.post('/categories/add', data={'name': 'Python'})
    logging.debug("Category added")

    # Add a flashcard
    response = test_client.post('/flashcards/add', data={
        'question': 'What is Flask?',
        'answer': 'A web framework for Python.',
        'category': 1  # Assume 'Python' is category ID 1
    }, follow_redirects=True)
    logging.debug("Flashcard added")

    assert response.status_code == 200
    assert b'Flashcard added successfully!' in response.data

    # Verify the flashcard exists
    response = test_client.get('/flashcards/')
    assert b'What is Flask?' in response.data
    assert b'A web framework for Python.' in response.data

@pytest.mark.timeout(10)
def test_edit_flashcard(test_client):
    # Add initial data
    test_client.post('/categories/add', data={'name': 'Python'})
    test_client.post('/flashcards/add', data={
        'question': 'What is Flask?',
        'answer': 'A web framework for Python.',
        'category': 1
    })

    # Edit the flashcard
    response = test_client.post('/flashcards/edit/1', data={
        'question': 'What is Flask used for?',
        'answer': 'Building web applications.',
        'category': 1
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Flashcard updated successfully!' in response.data

    # Verify the update
    response = test_client.get('/flashcards/')
    assert b'What is Flask used for?' in response.data
    assert b'Building web applications.' in response.data

@pytest.mark.timeout(10)
def test_delete_flashcard(test_client):
    # Add initial data
    test_client.post('/categories/add', data={'name': 'Python'})
    test_client.post('/flashcards/add', data={
        'question': 'What is Flask?',
        'answer': 'A web framework for Python.',
        'category': 1
    })

    # Delete the flashcard
    response = test_client.post('/flashcards/delete/1', follow_redirects=True)

    assert response.status_code == 200
    assert b'Flashcard deleted successfully!' in response.data

    # Verify deletion
    response = test_client.get('/flashcards/')
    assert b'What is Flask?' not in response.data
