from ..views import auth
from pyramid.httpexceptions import HTTPFound


def test_default_response_auth_view(dummy_request):
    from ..views.auth import auth_view
    response = auth_view(dummy_request)
    assert response == {}


def test_default_response_code(dummy_request):
    assert dummy_request.status_code == 200


def test_auth_signin_view(dummy_request):
    dummy_request.GET = {
        'username': 'watman', 'password': 'whodat', 'email': 'some@gmail.com'
    }
    assert dummy_request.status_code == 200


def test_auth_signup_view(dummy_request):
    dummy_request.POST = {'username': 'watman', 'password': 'whodat', 'e12l': 'wat@wat.com'}
    dummy_request.method = 'POST'
    assert dummy_request.status_code == 200
    # assert isinstance(dummy_request, HTTPFound)


# def test_bad_request_method_auth_signup_view(dummy_request):
#     from ..views.default import auth_view
#     from pyramid.httpexceptions import HTTPFound
#
#     dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
#     dummy_request.method = 'POST'
#     response = auth(dummy_request)
#     assert response.status_code == 302
#     assert isinstance(response, HTTPFound)
