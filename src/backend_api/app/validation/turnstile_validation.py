from typing import Optional
from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from pydantic import TypeAdapter
from requests import HTTPError, post

import bcrypt


from app.core.schemas import TurnstileQuery, TurnstileResponse
from app.core.models.models import TemporaryHashedUserIP as model_TemporaryHashedUserIP
from app.core.config import settings


class ValidateTurnstileRequest:
    def __init__(self):
        self.validate = TypeAdapter(TurnstileResponse).validate_python
        self.turnstile_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        self.turnstile_secret_key = settings.TURNSTILE_SECRET_KEY

    def _create_hashed_ip(request_data_ip: str) -> None:
        """Temporary storage of hashed ip address for 24 hours time period.
        IPs are hashed to protect user privacy.
        They are used to secure the turnstile endpoint from abuse.
        """
        salt = bcrypt.gensalt()

        hashed_ip = bcrypt.hashpw(request_data_ip.encode(), salt)

        return hashed_ip

    def _get_hashed_ip_statement(self, db: Session) -> Select:
        statement = select(
            model_TemporaryHashedUserIP.hashedIp, model_TemporaryHashedUserIP.createdAt
        )
        return statement

    def _add_hashed_ip_to_db(self, db: Session, hashed_ip: str) -> None:
        hashed_ip_map = {"hashedIp": hashed_ip}

        hashed_ip_obj = model_TemporaryHashedUserIP(**hashed_ip_map)

        db.add(hashed_ip_obj)
        db.commit()

    async def validate_turnstile_request(
        self, db: Session, *, request_data: TurnstileQuery
    ) -> TurnstileResponse:
        body = {
            "secret": self.turnstile_secret_key,
            "response": request_data.token,
            "remoteip": request_data.ip,
        }

        ip = request_data.ip

        statement = self._get_hashed_ip_statement(db)

        all_hashes = db.execute(statement).mappings().all()

        for hashed_ip in all_hashes:
            if bcrypt.checkpw(password=ip, hashed_password=hashed_ip["hashedIp"]):
                print("IP already exists in database")
                outcome = {"success": True}
                return self.validate(outcome)

        try:
            result = post(self.turnstile_url, json=body, headers={"Content-Type": "application/json"})
        except Exception as e:
            raise HTTPError(
                f"""Failed to send challenge request to cloudflare turnstile
                endpoint with error: {e}"""
            )

        outcome = result.json()
        if outcome["success"]:
            hashed_ip = self._create_hashed_ip(ip)

            self._add_hashed_ip_to_db(db, hashed_ip)
            return self.validate(outcome)
        else:
            raise HTTPError(
                f'Failed validation in turnstile request with error: {outcome["error-codes"]}'
            )
