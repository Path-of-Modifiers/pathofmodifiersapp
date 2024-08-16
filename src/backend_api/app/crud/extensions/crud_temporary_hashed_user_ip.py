import bcrypt


from sqlalchemy import Select, select
from sqlalchemy.orm import Session


from app.core.schemas.hashed_user_ip import (
    HashedUserIpCreate,
    HashedUserIp,
    HashedUserIpQuery,
)
from app.core.models.models import TemporaryHashedUserIP as model_TemporaryHashedUserIP
from app.crud.base import CRUDBase


class CRUDTemporaryHashedUserIp(
    CRUDBase[
        model_TemporaryHashedUserIP,
        HashedUserIp,
        HashedUserIpCreate,
        HashedUserIpQuery,
    ]
):
    async def check_temporary_hashed_ip(self, db: Session, ip: str) -> bool:
        """Check temporary hashed IP in the database.

        Args:
            db (Session): DB session.
            temporary_hashed_user_ip_query (HashedUserIpQuery): Temporary hashed user IP query.

        Returns:
            bool: True if the IP is in the database, False otherwise.
        """
        get_hashed_ip_map = {"hashedIp": ip}

        all_hashes = self.get(db=db, filter=get_hashed_ip_map)

        for hashed_ip in all_hashes:
            encoded_ip = ip.encode("utf-8")
            encoded_hashed_ip = hashed_ip["hashedIp"].encode("utf-8")
            if bcrypt.checkpw(encoded_ip, encoded_hashed_ip):
                return True

        return False