from typing import List
import bcrypt

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.core.schemas import HashedUserIpCreate
from app.core.models.models import TemporaryHashedUserIP as model_TemporaryHashedUserIP


class HashedIpValidation:
    def _get_temporary_hashed_ip_statement(self) -> Select:
        """Get temporary hashed IP statement.

        Returns:
            Select: Temporary hashed IP statement.
        """
        statement = select(
            model_TemporaryHashedUserIP.hashedIp, model_TemporaryHashedUserIP.createdAt
        )
        return statement

    def get_all_temporary_hashed_user_ips(self, db: Session) -> List:
        """Get all temporary hashed user IPs.

        Args:
            db (Session): DB session.

        Returns:
            List: List of all temporary hashed user IPs.
        """
        statement = self._get_temporary_hashed_ip_statement()

        all_hashes = db.execute(statement).mappings().all()

        return all_hashes

    def add_temporary_hashed_ip_to_db(self, db: Session, hashed_ip: str) -> None:
        """Adds a hashed IP to the temporary hashed IP table.

        Args:
            db (Session): DB session.
            hashed_ip (str): Hashed IP.
        """
        hashed_ip_map = {"hashedIp": hashed_ip}

        obj_create = HashedUserIpCreate(**hashed_ip_map)

        db_obj = model_TemporaryHashedUserIP(**obj_create.model_dump())

        db.add(db_obj)
        db.commit()

    def create_hashed_ip(self, request_data_ip: str) -> str:
        """
        IPs are hashed to protect user privacy.
        They are used to secure the turnstile endpoint from abuse.
        """
        salt = bcrypt.gensalt()

        encoded_ip = request_data_ip.encode("utf-8")

        hashed_ip = bcrypt.hashpw(encoded_ip, salt)

        hashed_ip = hashed_ip.decode("utf-8")

        return hashed_ip

    def check_temporary_hashed_ip(self, db: Session, ip: str) -> bool:
        """Check temporary hashed IP in the database.

        Args:
            db (Session): DB session.
            ip (str): IP address.

        Returns:
            bool: True if the IP is in the database, False otherwise.
        """
        statement = self._get_temporary_hashed_ip_statement()

        all_hashes = db.execute(statement).mappings().all()

        for hashed_ip in all_hashes:
            encoded_ip = ip.encode("utf-8")
            encoded_hashed_ip = hashed_ip["hashedIp"].encode("utf-8")
            if bcrypt.checkpw(encoded_ip, encoded_hashed_ip):
                return True

        return False
