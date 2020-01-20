from microservices.note import Note


def test_create_note():
    n = Note()
    data = {
        "id": "25",
        "Title": "AppFundoo",
        "Description": "user api development",
        "Colour": "Green",
        "isPinned": "0",
        "isArchive": "0",
        "isTrash": "0"
    }
    assert n.create_note(data) == {'success': True, 'data': [], 'message': "Entry already available"}


def test_delete_note():
    n = Note()
    data = {
        "id": "24"
    }
    assert n.delete_note(data) == {'success': True, 'data': [], 'message': "Entry Delete Successfully"}


def test_update_note():
    n = Note()
    data = {
        "id": "24",
        "Title": "ApppFuuun",
        "Description": "user api development",
        "Colour": "Green",
        "isPinned": "0",
        "isArchive": "0",
        "isTrash": "0"
    }
    assert n.update_note(data) == {'success': True, 'data': [], 'message': "Data Update Successfully"}


def test_read_note():
    n = Note()
    data = {
        "id": "24"
    }
    assert n.read_note(data) == {'success': True, 'data': [], 'message': "Data read Successfully"}