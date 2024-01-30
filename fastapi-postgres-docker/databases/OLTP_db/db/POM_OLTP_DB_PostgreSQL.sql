CREATE TABLE "Currency" (
  "currency_name" varchar PRIMARY KEY,
  "value_in_chaos" float NOT NULL,
  "icon_url" varchar NOT NULL,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "Item" (
  "item_id" varchar PRIMARY KEY, 
  "stash_id" varchar NOT NULL,
  "name" varchar,
  "icon_url" varchar,
  "league" varchar NOT NULL,
  "type_line" varchar NOT NULL,
  "rarity" varchar NOT NULL,
  "identified" boolean NOT NULL,
  "item_level" smallint NOT NULL,
  "forum_note" varchar,
  "currency_amount" float(24),
  "currency_name" varchar,
  "corrupted" boolean,
  "delve" boolean,
  "fractured" boolean,
  "synthesized" boolean,
  "replica" boolean,
  "elder" boolean,
  "shaper" boolean,
  "searing" boolean,
  "tangled" boolean,
  "influences" jsonb,
  "is_relic" boolean,
  "prefixes" smallint,
  "suffixes" smallint,
  "foil_variation" int,
  "inventory_id" varchar,
  "created_at" datetime,
  "updated_at" datetime,
  FOREIGN KEY (base_type) REFERENCES Item_Basetype(basetype) ON DELETE RESTRICT,
  FOREIGN KEY (currency_name) REFERENCES Currency(currency_name) ON DELETE RESTRICT,
  FOREIGN KEY (stash_id) REFERENCES Stash(stash_id) ON DELETE CASCADE
);

CREATE TABLE "Transaction" (
  "transaction_id" serial PRIMARY KEY, 
  "item_id" varchar NOT NULL,
  "account_name" varchar NOT NULL,
  "currency_amount" float(24) NOT NULL,
  "currency_name" varchar NOT NULL,
  "created_at" datetime,
  "updated_at" datetime,
  FOREIGN KEY (item_id) REFERENCES Item(item_id) ON DELETE CASCADE,
  FOREIGN KEY (account_name) REFERENCES Account(account_name) ON DELETE CASCADE,
  FOREIGN KEY (currency_name) REFERENCES Currency(currency_name) ON DELETE RESTRICT
);

CREATE TABLE "Item_Basetype" (
  "base_type" varchar PRIMARY KEY,
  "category" varchar NOT NULL,
  "sub_category" jsonb NOT NULL,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "Item_Modifiers" (
  "modifier_id" varchar PRIMARY KEY,
  "item_id" varchar PRIMARY KEY,
  FOREIGN KEY (modifier_id) REFERENCES Modifier(modifier_id) ON DELETE CASCADE,
  FOREIGN KEY (item_id) REFERENCES Item(item_id) ON DELETE CASCADE
);

CREATE TABLE "Modifier" (
  "modifier_id" varchar PRIMARY KEY, 
  "effect" varchar NOT NULL,
  "implicit" boolean,
  "explicit" boolean,
  "delve" boolean,
  "fractured" boolean,
  "synthesized" boolean,
  "corrupted" boolean,
  "enchanted" boolean,
  "veiled" boolean,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "Modifier_Stats" (
  "modifier_id" varchar PRIMARY KEY,
  "stat_id" varchar PRIMARY KEY,
  FOREIGN KEY (modifier_id) REFERENCES Modifier(modifier_id) ON DELETE CASCADE,
  FOREIGN KEY (stat_id) REFERENCES Stat(stat_id) ON DELETE CASCADE
);

CREATE TABLE "Stat" (
  "stat_id" varchar PRIMARY KEY, 
  "position" smallint NOT NULL PRIMARY KEY, 
  "stat_value" smallint NOT NULL, 
  "mininum_value" smallint,
  "maximum_value" smallint,
  "stat_tier" smallint, 
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "Stash" (
  "stash_id" varchar PRIMARY KEY, 
  "account_name" varchar NOT NULL,
  "public" boolean NOT NULL,
  "league" varchar NOT NULL,
  "created_at" datetime,
  "updated_at" datetime,
  FOREIGN KEY (account_name) REFERENCES Account(account_name) ON DELETE CASCADE
);

CREATE TABLE "Account" (
  "account_name" varchar PRIMARY KEY,
  "is_banned" boolean,
  "created_at" datetime,
  "updated_at" datetime
);