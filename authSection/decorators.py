from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def uploader_required(function=None,redirect_field_name = REDIRECT_FIELD_NAME, login_url='login'):
    '''
         This decorator will check that the logged user is a uploader
    '''
    actual_decorator =user_passes_test(
        lambda u: u.is_active and u.groups.filter(name='Uploader').exists(),
        login_url=login_url,
        redirect_field_name = redirect_field_name
    )

    if function:
        return actual_decorator(function)

    return actual_decorator    



def office_required(function=None,redirect_field_name = REDIRECT_FIELD_NAME, login_url='login'):
    '''
         This decorator will check that the logged user is a office staff
    '''
    actual_decorator =user_passes_test(
        lambda u: u.is_active and u.groups.filter(name='Office').exists(),
        login_url=login_url,
        redirect_field_name = redirect_field_name
    )

    if function:
        return actual_decorator(function)

    return actual_decorator   



def stores_required(function=None,redirect_field_name = REDIRECT_FIELD_NAME, login_url='login'):
    '''
         This decorator will check that the logged user is a store staff
    '''
    actual_decorator =user_passes_test(
        lambda u: u.is_active and u.groups.filter(name='Stores').exists(),
        login_url=login_url,
        redirect_field_name = redirect_field_name
    )

    if function:
        return actual_decorator(function)

    return actual_decorator   
