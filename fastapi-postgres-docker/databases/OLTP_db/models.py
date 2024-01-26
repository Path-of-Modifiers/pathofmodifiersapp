import database as _database
from sqlalchemy.dialects.postgresql import JSONB

class Currency(_database.Base):

    __tablename__ = 'Currency'

    currency_name = _database.Column(_database.String(), primary_key=True)
    value_in_chaos = _database.Column(_database.Float(), nullable=False)
    icon_url = _database.Column(_database.String(), nullable=False)
    created_at = _database.Column(_database.DateTime())
    updated_at = _database.Column(_database.DateTime())


class Item(_database.Base):

    __tablename__ = 'Item'

    item_id = _database.Column(_database.String(), primary_key=True)
    stash_id = _database.Column(_database.String(), _database.ForeignKey('Stash.stash_id'), ondelete="CASCADE", nullable=False)
    name = _database.Column(_database.String())
    icon_url = _database.Column(_database.String())
    league = _database.Column(_database.String(), nullable=False)
    base_type = _database.Column(_database.String(), nullable=False)
    type_line = _database.Column(_database.String(), nullable=False)
    rarity = _database.Column(_database.String(), nullable=False)
    identified = _database.Column(_database.Boolean(), nullable=False)
    item_level = _database.Column(_database.SmallInteger(), nullable=False)
    forum_note = _database.Column(_database.String())
    currency_amount = _database.Column(_database.Float(24))
    currency_name = _database.Column(_database.String(), _database.ForeignKey('Currency.currency_name'), ondelete="RESTRICT")
    corrupted = _database.Column(_database.Boolean())
    delve = _database.Column(_database.Boolean())
    fractured = _database.Column(_database.Boolean())
    synthesized = _database.Column(_database.Boolean())
    replica = _database.Column(_database.Boolean())
    elder = _database.Column(_database.Boolean())
    shaper = _database.Column(_database.Boolean())
    searing = _database.Column(_database.Boolean())
    tangled = _database.Column(_database.Boolean())
    influences = _database.Column(JSONB())
    is_relic = _database.Column(_database.Boolean())
    prefixes = _database.Column(_database.SmallInteger())
    suffixes = _database.Column(_database.SmallInteger())
    foil_variation = _database.Column(_database.Integer())
    inventory_id = _database.Column(_database.String())
    created_at = _database.Column(_database.DateTime())
    updated_at = _database.Column(_database.DateTime())


class Transaction(_database.Base):

    __tablename__ = 'Transaction'

    transaction_id = _database.Column(_database.Integer(), autoincrement=True, primary_key=True)
    item_id = _database.Column(_database.String(), _database.ForeignKey('Item.item_id'), ondelete="CASCADE", nullable=False)
    account_name = _database.Column(_database.String(), _database.ForeignKey('Account.account_name'), ondelete="CASCADE", nullable=False)
    currency_amount = _database.Column(_database.Float(24), nullable=False)
    currency_name = _database.Column(_database.String(), _database.ForeignKey('Currency.currency_name'), ondelete="RESTRICT", nullable=False)
    created_at = _database.Column(_database.DateTime())
    updated_at = _database.Column(_database.DateTime())


class ItemCategories(_database.Base):

    __tablename__ = 'Item_Categories'

    category_name = _database.Column(_database.String(), _database.ForeignKey('Category.category_name'), ondelete="CASCADE", primary_key=True)
    item_id = _database.Column(_database.String(), _database.ForeignKey('Item.item_id'), ondelete="CASCADE", primary_key=True)


class ItemModifiers(_database.Base):

    __tablename__ = 'Item_Modifiers'

    modifier_id = _database.Column(_database.String(), _database.ForeignKey('Modifier.modifier_id'), ondelete="CASCADE", primary_key=True)
    item_id = _database.Column(_database.String(), _database.ForeignKey('Item.item_id'), ondelete="CASCADE", primary_key=True)


class Category(_database.Base):

    __tablename__ = 'Category'

    category_name = _database.Column(_database.String(), primary_key=True)
    is_sub_category = _database.Column(_database.Boolean())


class Modifier(_database.Base):

    __tablename__ = 'Modifier'

    modifier_id = _database.Column(_database.String(), primary_key=True)
    effect = _database.Column(_database.String(), nullable=False)
    implicit = _database.Column(_database.Boolean())
    explicit = _database.Column(_database.Boolean())
    delve = _database.Column(_database.Boolean())
    fractured = _database.Column(_database.Boolean())
    synthesized = _database.Column(_database.Boolean())
    corrupted = _database.Column(_database.Boolean())
    enchanted = _database.Column(_database.Boolean())
    veiled = _database.Column(_database.Boolean())
    created_at = _database.Column(_database.DateTime())
    updated_at = _database.Column(_database.DateTime())


class ModifierStats(_database.Base):

    __tablename__ = 'Modifier_Stats'

    modifier_id = _database.Column(_database.String(), _database.ForeignKey('Modifier.modifier_id'), ondelete="CASCADE", primary_key=True)
    stat_id = _database.Column(_database.String(), _database.ForeignKey('Stat.stat_id'), ondelete="CASCADE", primary_key=True)


class Stat(_database.Base):

    __tablename__ = 'Stat'

    stat_id = _database.Column(_database.String(), primary_key=True)
    position = _database.Column(_database.SmallInteger(), primary_key=True)
    stat_value = _database.Column(_database.SmallInteger(), nullable=False)
    mininum_value = _database.Column(_database.SmallInteger())
    maximum_value = _database.Column(_database.SmallInteger())
    stat_tier = _database.Column(_database.SmallInteger())
    created_at = _database.Column(_database.DateTime())
    updated_at = _database.Column(_database.DateTime())


class Stash(_database.Base):

    __tablename__ = 'Stash'

    stash_id = _database.Column(_database.String(), primary_key=True)
    account_name = _database.Column(_database.String(), _database.ForeignKey('Account.account_name'), ondelete="CASCADE", nullable=False)
    public = _database.Column(_database.Boolean(), nullable=False)
    league = _database.Column(_database.String(), nullable=False)
    created_at = _database.Column(_database.DateTime())
    updated_at = _database.Column(_database.DateTime())


class Account(_database.Base):

    __tablename__ = 'Account'

    account_name = _database.Column(_database.String(), primary_key=True)
    is_banned = _database.Column(_database.Boolean())
    created_at = _database.Column(_database.DateTime())
    updated_at = _database.Column(_database.DateTime())
