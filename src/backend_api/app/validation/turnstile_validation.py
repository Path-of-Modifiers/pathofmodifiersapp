from sqlalchemy.orm import Session
from pydantic import TypeAdapter
from requests import HTTPError, post

from app.core.schemas import TurnstileQuery, TurnstileResponse
from app.core.config import settings
from app.validation.hashed_ip_validation import HashedIpValidation


class ValidateTurnstileRequest:
    def __init__(self):
        self.validate = TypeAdapter(TurnstileResponse).validate_python
        self.turnstile_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        self.turnstile_secret_key = settings.TURNSTILE_SECRET_KEY
        self.hashed_ip_validation_tool = HashedIpValidation()

    async def validate_turnstile_request(
        self, db: Session, *, request_data: TurnstileQuery
    ) -> TurnstileResponse:
        body = {
            "secret": self.turnstile_secret_key,
            "response": request_data.token,
            "remoteip": request_data.ip,
        }

        ip = request_data.ip

        check_temporary_hashed_ip = (
            self.hashed_ip_validation_tool.check_temporary_hashed_ip(db, ip)
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
            hashed_ip = self.hashed_ip_validation_tool.create_hashed_ip(ip)
            self.hashed_ip_validation_tool.add_temporary_hashed_ip_to_db(db, hashed_ip)

            return self.validate(outcome)
        else:
            raise HTTPError(
                f'Failed validation in turnstile request with error: {outcome["error-codes"]}'
            )
