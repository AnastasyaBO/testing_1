import os
from testing_1.petfriend.api import PetFriends
from testing_1.petfriend.settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Вход в систему"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_valid_user_negative(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 400


def test_get_api_key_password_is_none(email=valid_email):
    """Вход в систему без ввода пароля"""
    status, result = pf.get_api_key_password_is_none(email)
    assert status == 200


def test_get_api_key_email_is_none(password=valid_password):
    """Вход в систему без ввода почты"""
    status, result = pf.get_api_key_email_is_none(password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=""):
    """Получение полного списка питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_valid_key_negative(filter=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 400


def test_add_new_pet_with_valid_data(name="Mos'ka", animal_type='Cat', age='4', pet_photo='images/sad_cat.jpeg'):
    """Добавление нового питомца в систему с фото"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_name_type_age_with_valid_data(name='', animal_type='', age='', pet_photo='images/sad_cat.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_successful_delete_self_pet():
    """Удаление питомца из системы"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "GoodFriend", "Cat", "3", "images/sad_cat.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_delete_self_pet_negative():
    """Удаление питомца с индексом 0"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "Lilit", "kitty cat", "3", "images/sad_cat.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 400


def test_successful_delete_more_index_self_pet():
    """Попытка удалить питомца, если в разделе "my_pets" меньше питомцев, заданного индекса"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "GoodFriend", "Cat", "3", "images/sad_cat.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][4]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name="Кошатина", animal_type='кот', age='2'):
    """Изменение информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_update_self_pet_info_negativ(name="Кошатина", animal_type='кот', age='2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400


def test_add_new_pet_without_photo(name='Mars', animal_type='cat', age='2'):
    """Добавление нового питомца в систему с без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_photo_negative(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name


def test_add_photo_of_a_pet(pet_photo='images/little_cat.jpg'):
    """Добавление фото к существующей анкете питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet_without_photo(auth_key, "", "", "")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_add_photo_of_a_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo']


def test_add_photo_of_a_pet_negative(pet_photo='images/little_cat.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet_without_photo(auth_key, "", "", "")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_add_photo_of_a_pet(auth_key, pet_id, pet_photo)

    assert status == 400



















