from views import web_views  # noqa
import mock
import responses

from tests.helpers.rest_utils import post_json, json_of_response
from tests.helpers.eth_utils import sample_eth_address, str_eth


from database import db_models
VC = db_models.VerificationCode


def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_request_phone_verify(client):
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            'https://api.authy.com/protected/json/phones/verification/start',
            status=200
        )

        args = {
            'country_calling_code': '1',
            'phone': '12341234',
            'method': 'sms'
        }
        response = post_json(client, '/api/attestations/phone/generate-code',
                             args)

        assert response.status_code == 200
        assert json_of_response(response) == {}


@responses.activate
def test_verify_phone(client):
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            'https://api.authy.com/protected/json/phones/verification/status',
            json={
                'message': 'Verification code is correct.',
                'success': True
            }
        )

        args = {
            'country_calling_code': '1',
            'phone': '12341234',
            'code': '123456',
            'identity': str_eth(sample_eth_address)
        }
        response = post_json(client, '/api/attestations/phone/verify', args)

        assert response.status_code == 200
        response_json = json_of_response(response)
        assert len(response_json['signature']) == 132
        assert response_json['data'] == 'phone verified'


@mock.patch('python_http_client.client.Client')
def test_email_verify(MockHttpClient, client):
    email = 'test@dumb.bo'
    resp = post_json(client,
                     "/api/attestations/email/generate-code",
                     {"email": email})

    db_code = VC.query.filter(VC.email == email).first()
    assert db_code.code is not None

    resp = post_json(client,
                     "/api/attestations/email/verify",
                     {"email": email,
                      "identity": str_eth(sample_eth_address),
                      'code': db_code.code})
    resp_json = json_of_response(resp)
    assert resp.status_code == 200
    assert len(resp_json['signature']) == 132
    assert resp_json['data'] == 'email verified'


@mock.patch("http.client.HTTPSConnection")
def test_facebook_verify(MockHttpConnection, client):
    mock_http_conn = mock.Mock()
    mock_get_response = mock.Mock()
    mock_get_response.read.return_value = '{"access_token": "foo"}'
    mock_http_conn.getresponse.return_value = mock_get_response
    MockHttpConnection.return_value = mock_http_conn

    resp = client.get(
        "/api/attestations/facebook/auth-url")
    expected_url = ("?client_id=facebook-client-id&redirect_uri"
                    "=https://testhost.com/redirects/facebook/")
    assert resp.status_code == 200
    assert expected_url in json_of_response(resp)['url']

    resp = post_json(client,
                     "/api/attestations/facebook/verify",
                     {"identity": str_eth(sample_eth_address),
                      "code": "abcde12345"})
    resp_json = json_of_response(resp)
    assert resp.status_code == 200
    assert len(resp_json['signature']) == 132
    assert resp_json['data'] == 'facebook verified'


@mock.patch('logic.attestation_service.requests')
def test_twitter_verify(mock_requests, client):
    response_content = b'oauth_token=peaches&oauth_token_secret=pears'
    mock_requests.post().content = response_content
    mock_requests.post().status_code = 200

    resp = client.get(
        "/api/attestations/twitter/auth-url")
    expected_url = "oauth_token=peaches"
    assert resp.status_code == 200
    assert expected_url in json_of_response(resp)['url']

    resp = post_json(client,
                     "/api/attestations/twitter/verify",
                     {"identity": str_eth(sample_eth_address),
                      "oauth-verifier": "abcde12345"})
    resp_json = json_of_response(resp)
    assert resp.status_code == 200
    assert len(resp_json['signature']) == 132
    assert resp_json['data'] == 'twitter verified'
