from django.urls import reverse


def compute_auth_header(client, mail_utilisateur, pass_utilisateur):
    url_login = reverse('login')
    response_login = client.post(url_login, {
        "email": mail_utilisateur,
        "password": pass_utilisateur
    }, format='json')

    auth_headers = {
        'HTTP_AUTHORIZATION': 'Bearer ' + (response_login.data["token"].decode()),
    }

    return auth_headers