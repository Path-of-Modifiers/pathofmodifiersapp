import database as _database
import sqlalchemy as _sql
from sqlalchemy.dialects.postgresql import JSONB

class Currency(_database.Base):

    __tablename__ = 'Currency'

    currency_name = _sql.Column(_sql.String(), primary_key=True)
    value_in_chaos = _sql.Column(_sql.Float(), nullable=False)
    icon_url = _sql.Column(_sql.String(), nullable=False)
    created_at = _sql.Column(_sql.DateTime())
    updated_at = _sql.Column(_sql.DateTime())


class Item(_database.Base):

    __tablename__ = 'Item'

    item_id = _sql.Column(_sql.String(), primary_key=True)
    stash_id = _sql.Column(_sql.String(), _sql.ForeignKey('Stash.stash_id'), ondelete="CASCADE", nullable=False)
    name = _sql.Column(_sql.String())
    icon_url = _sql.Column(_sql.String())
    league = _sql.Column(_sql.String(), nullable=False)
    base_type = _sql.Column(_sql.String(), nullable=False)
    type_line = _sql.Column(_sql.String(), nullable=False)
    rarity = _sql.Column(_sql.String(), nullable=False)
    identified = _sql.Column(_sql.Boolean(), nullable=False)
    item_level = _sql.Column(_sql.SmallInteger(), nullable=False)
    forum_note = _sql.Column(_sql.String())
    currency_amount = _sql.Column(_sql.Float(24))
    currency_name = _sql.Column(_sql.String(), _sql.ForeignKey('Currency.currency_name'), ondelete="RESTRICT")
    corrupted = _sql.Column(_sql.Boolean())
    delve = _sql.Column(_sql.Boolean())
    fractured = _sql.Column(_sql.Boolean())
    synthesized = _sql.Column(_sql.Boolean())
    replica = _sql.Column(_sql.Boolean())
    elder = _sql.Column(_sql.Boolean())
    shaper = _sql.Column(_sql.Boolean())
    searing = _sql.Column(_sql.Boolean())
    tangled = _sql.Column(_sql.Boolean())
    influences = _sql.Column(JSONB())
    is_relic = _sql.Column(_sql.Boolean())
    prefixes = _sql.Column(_sql.SmallInteger())
    suffixes = _sql.Column(_sql.SmallInteger())
    foil_variation = _sql.Column(_sql.Integer())
    inventory_id = _sql.Column(_sql.String())
    created_at = _sql.Column(_sql.DateTime())
    updated_at = _sql.Column(_sql.DateTime())


class Transaction(_database.Base):

    __tablename__ = 'Transaction'

    transaction_id = _sql.Column(_sql.Integer(), autoincrement=True, primary_key=True)
    item_id = _sql.Column(_sql.String(), _sql.ForeignKey('Item.item_id'), ondelete="CASCADE", nullable=False)
    account_name = _sql.Column(_sql.String(), _sql.ForeignKey('Account.account_name'), ondelete="CASCADE", nullable=False)
    currency_amount = _sql.Column(_sql.Float(24), nullable=False)
    currency_name = _sql.Column(_sql.String(), _sql.ForeignKey('Currency.currency_name'), ondelete="RESTRICT", nullable=False)
    created_at = _sql.Column(_sql.DateTime())
    updated_at = _sql.Column(_sql.DateTime())


class ItemCategories(_database.Base):

    __tablename__ = 'Item_Categories'

    category_name = _sql.Column(_sql.String(), _sql.ForeignKey('Category.category_name'), ondelete="CASCADE", primary_key=True)
    item_id = _sql.Column(_sql.String(), _sql.ForeignKey('Item.item_id'), ondelete="CASCADE", primary_key=True)


class ItemModifiers(_database.Base):

    __tablename__ = 'Item_Modifiers'

    modifier_id = _sql.Column(_sql.String(), _sql.ForeignKey('Modifier.modifier_id'), ondelete="CASCADE", primary_key=True)
    item_id = _sql.Column(_sql.String(), _sql.ForeignKey('Item.item_id'), ondelete="CASCADE", primary_key=True)


class Category(_database.Base):

    __tablename__ = 'Category'

    category_name = _sql.Column(_sql.String(), primary_key=True)
    is_sub_category = _sql.Column(_sql.Boolean())


class Modifier(_database.Base):

    __tablename__ = 'Modifier'

    modifier_id = _sql.Column(_sql.String(), primary_key=True)
    effect = _sql.Column(_sql.String(), nullable=False)
    implicit = _sql.Column(_sql.Boolean())
    explicit = _sql.Column(_sql.Boolean())
    delve = _sql.Column(_sql.Boolean())
    fractured = _sql.Column(_sql.Boolean())
    synthesized = _sql.Column(_sql.Boolean())
    corrupted = _sql.Column(_sql.Boolean())
    enchanted = _sql.Column(_sql.Boolean())
    veiled = _sql.Column(_sql.Boolean())
    created_at = _sql.Column(_sql.DateTime())
    updated_at = _sql.Column(_sql.DateTime())


class ModifierStats(_database.Base):

    __tablename__ = 'Modifier_Stats'

    modifier_id = _sql.Column(_sql.String(), _sql.ForeignKey('Modifier.modifier_id'), ondelete="CASCADE", primary_key=True)
    stat_id = _sql.Column(_sql.String(), _sql.ForeignKey('Stat.stat_id'), ondelete="CASCADE", primary_key=True)


class Stat(_database.Base):

    __tablename__ = 'Stat'

    stat_id = _sql.Column(_sql.String(), primary_key=True)
    position = _sql.Column(_sql.SmallInteger(), primary_key=True)
    stat_value = _sql.Column(_sql.SmallInteger(), nullable=False)
    mininum_value = _sql.Column(_sql.SmallInteger())
    maximum_value = _sql.Column(_sql.SmallInteger())
    stat_tier = _sql.Column(_sql.SmallInteger())
    created_at = _sql.Column(_sql.DateTime())
    updated_at = _sql.Column(_sql.DateTime())


class Stash(_database.Base):

    __tablename__ = 'Stash'

    stash_id = _sql.Column(_sql.String(), primary_key=True)
    account_name = _sql.Column(_sql.String(), _sql.ForeignKey('Account.account_name'), ondelete="CASCADE", nullable=False)
    public = _sql.Column(_sql.Boolean(), nullable=False)
    league = _sql.Column(_sql.String(), nullable=False)
    created_at = _sql.Column(_sql.DateTime())
    updated_at = _sql.Column(_sql.DateTime())


class Account(_database.Base):

    __tablename__ = 'Account'

    account_name = _sql.Column(_sql.String(), primary_key=True)
    is_banned = _sql.Column(_sql.Boolean())
    created_at = _sql.Column(_sql.DateTime())
    updated_at = _sql.Column(_sql.DateTime())
