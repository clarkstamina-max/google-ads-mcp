def _create_credentials() -> google.auth.credentials.Credentials:
    """Returns credentials from env vars, FastMCP token, or ADC."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    client_id = os.environ.get("GOOGLE_ADS_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_ADS_CLIENT_SECRET")
    refresh_token = os.environ.get("GOOGLE_ADS_REFRESH_TOKEN")

    if client_id and client_secret and refresh_token:
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=[_ADS_SCOPE],
        )
        creds.refresh(Request())
        return creds

    from fastmcp.server.dependencies import get_access_token
    token_obj = get_access_token()
    if token_obj and token_obj.token:
        return Credentials(token=token_obj.token)

    credentials, _ = google.auth.default(scopes=[_ADS_SCOPE])
    return credentials
