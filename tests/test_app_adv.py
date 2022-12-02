import pytest
from tests import api


def test_create_get_advertisement(new_user):
    token = api.login(new_user['name'], new_user['password'])['token']
    title = 'New title!'
    new_adv = api.create_adv(token=token,
                             title=title,
                             description='This is a new tittle description.'
                             )

    assert 'id' in new_adv

    adv_data = api.get_adv(new_adv.get("id"))

    assert adv_data['Title'] == title


def test_get_advertisement(new_adv):
    adv_data = api.get_adv(new_adv['id'])

    assert adv_data['Title'] == new_adv['title']


def test_patch_adv(new_adv):
    response = api.patch_adv(new_adv['token'],
                             {'title': new_adv['title'],
                              'description': 'This is a new description for old title.'})
    assert response == {"status": "success"}

    adv = api.get_adv(new_adv['id'])
    assert adv['Description'] == 'This is a new description for old title.'


def test_delete_adv(new_adv):
    response = api.delete_adv(new_adv['id'], new_adv['token'])
    assert response == {"status": "success"}

    with pytest.raises(api.ApiError) as err_info:
        api.get_adv(new_adv['id'])

    assert err_info.value.status_code == 404
    assert err_info.value.message == {'status': 'error',
                                      'message': 'AdvModel not found'}
