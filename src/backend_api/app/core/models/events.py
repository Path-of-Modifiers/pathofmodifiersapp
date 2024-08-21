from sqlalchemy import DDL, event

from app.core.models.models import TemporaryHashedUserIP

delete_row_after_24_hours = DDL(
    """\
CREATE FUNCTION temporary_hashed_user_ip_delete_old_rows() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  DELETE FROM temporary_hashed_user_ip
  WHERE temporary_hashed_user_ip."createdAt" < NOW() - INTERVAL '24 hours';
  RETURN NEW;
END;

$$;

CREATE TRIGGER temporary_hashed_user_ip_delete_old_rows_trigger
    AFTER INSERT ON temporary_hashed_user_ip
    EXECUTE PROCEDURE temporary_hashed_user_ip_delete_old_rows();
"""
)


event.listen(
    TemporaryHashedUserIP.__tablename__, "after_insert", delete_row_after_24_hours
)
