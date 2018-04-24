import apilib


class GeneratePhoneVerificationCodeRequest(apilib.Request):
    eth_address = apilib.Field(apilib.String(), required=True)
    phone = apilib.Field(apilib.String(), required=True)


class GeneratePhoneVerificationCodeResponse(apilib.Response):
    pass


class VerifyPhoneRequest(apilib.Request):
    eth_address = apilib.Field(apilib.String(), required=True)
    phone = apilib.Field(apilib.String(), required=True)
    code = apilib.Field(apilib.String(), required=True)


class VerifyPhoneResponse(apilib.Response):
    # A successful response will have response_code SUCCESS.
    # Any invalid code with have response_code REQUEST_ERROR
    # and the 'errors' list will be populated.
    signature = apilib.Field(apilib.String())
    claim_type = apilib.Field(apilib.String())
    data = apilib.Field(apilib.String())


class GenerateEmailVerificationCodeRequest(apilib.Request):
    eth_address = apilib.Field(apilib.String(), required=True)
    email = apilib.Field(apilib.String(), required=True)


class GenerateEmailVerificationCodeResponse(apilib.Response):
    pass


class VerifyEmailRequest(apilib.Request):
    eth_address = apilib.Field(apilib.String(), required=True)
    email = apilib.Field(apilib.String(), required=True)
    code = apilib.Field(apilib.String(), required=True)


class VerifyEmailResponse(apilib.Response):
    signature = apilib.Field(apilib.String())
    claim_type = apilib.Field(apilib.String())
    data = apilib.Field(apilib.String())


class FacebookAuthUrlRequest(apilib.Request):
    redirect_url = apilib.Field(apilib.String(), required=True)


class FacebookAuthUrlResponse(apilib.Response):
    url = apilib.Field(apilib.String())


class VerifyFacebookRequest(apilib.Request):
    eth_address = apilib.Field(apilib.String(), required=True)
    code = apilib.Field(apilib.String(), required=True)
    redirect_url = apilib.Field(apilib.String(), required=True)


class VerifyFacebookResponse(apilib.Response):
    signature = apilib.Field(apilib.String())
    claim_type = apilib.Field(apilib.String())
    data = apilib.Field(apilib.String())


class TwitterAuthUrlRequest(apilib.Request):
    pass


class TwitterAuthUrlResponse(apilib.Response):
    url = apilib.Field(apilib.String())


class VerifyTwitterRequest(apilib.Request):
    eth_address = apilib.Field(apilib.String(), required=True)
    oauth_verifier = apilib.Field(apilib.String(), required=True)


class VerifyTwitterResponse(apilib.Response):
    signature = apilib.Field(apilib.String())
    claim_type = apilib.Field(apilib.String())
    data = apilib.Field(apilib.String())


class VerificationService(apilib.Service):
    path = '/api/verification_service'
    methods = apilib.servicemethods(
        apilib.Method(
            'generate_phone_verification_code',
            GeneratePhoneVerificationCodeRequest,
            GeneratePhoneVerificationCodeResponse),
        apilib.Method(
            'verify_phone',
            VerifyPhoneRequest,
            VerifyPhoneResponse),
        apilib.Method(
            'generate_email_verification_code',
            GenerateEmailVerificationCodeRequest,
            GenerateEmailVerificationCodeResponse),
        apilib.Method(
            'verify_email',
            VerifyEmailRequest,
            VerifyEmailResponse),
        apilib.Method(
            'facebook_auth_url',
            FacebookAuthUrlRequest,
            FacebookAuthUrlResponse),
        apilib.Method(
            'verify_facebook',
            VerifyFacebookRequest,
            VerifyFacebookResponse),
        apilib.Method(
            'twitter_auth_url',
            TwitterAuthUrlRequest,
            TwitterAuthUrlResponse),
        apilib.Method(
            'verify_twitter',
            VerifyTwitterRequest,
            VerifyTwitterResponse))
