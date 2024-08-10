from sqlalchemy.orm import Session
from pydantic import TypeAdapter
from requests import HTTPError, post

from app.core.schemas import TurnstileQuery, TurnstileResponse
from app.core.schemas.hashed_user_ip import HashedUserIpQuery
from app.core.config import settings
from app.validation.utils import create_hashed_ip
from app.crud import CRUD_hashed_user_ip


class ValidateTurnstileRequest:
    def __init__(self):
        self.validate = TypeAdapter(TurnstileResponse).validate_python
        self.turnstile_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        self.turnstile_secret_key = settings.TURNSTILE_SECRET_KEY

    async def validate_turnstile_request(
        self, db: Session, *, request_data: TurnstileQuery
    ) -> TurnstileResponse:
        body = {
            "secret": self.turnstile_secret_key,
            "response": request_data.token,
            "remoteip": request_data.ip,
        }

        ip = request_data.ip

        ip_query = HashedUserIpQuery(hashedIp=create_hashed_ip(ip))

        check_temporary_hashed_ip = await CRUD_hashed_user_ip.check_temporary_hashed_ip(
            db, ip_query
        )

        if check_temporary_hashed_ip:
            return self.validate({"success": True})

        try:
            result = post(
                self.turnstile_url,
                json=body,
                headers={"Content-Type": "application/json"},
            )
        except Exception as e:
            raise HTTPError(
                f"""Failed to send challenge request to cloudflare turnstile
                endpoint with error: {e}"""
            )

        outcome = result.json()
        if outcome["success"]:
            hashed_ip = create_hashed_ip(ip)
            hashed_ip_map = {"hashedIp": hashed_ip}
            await CRUD_hashed_user_ip.create(db, hashed_ip_map)

            return self.validate(outcome)
        else:
            raise HTTPError(
                f'Failed validation in turnstile request with error: {outcome["error-codes"]}'
            )
