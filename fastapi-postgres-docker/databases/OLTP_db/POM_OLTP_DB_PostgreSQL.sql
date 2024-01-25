CREATE TABLE "Currency" (
  "currency_name" varchar PRIMARY KEY, -- Self generated
  "value_in_chaos" float NOT NULL,
  "icon_url" varchar NOT NULL,
  "created_at" datetime,
  "updated_at" datetime
  FOREIGN KEY (icon_url) REFERENCES Icon(icon_url) ON DELETE SET NULL
);

CREATE TABLE "Item" (
  "item_id" varchar PRIMARY KEY, -- Field "id" in Item POE API object
  "stash_id" varchar NOT NULL,
  "name" varchar,
  "icon_url" varchar,
  "league" varchar NOT NULL,
  "base_type" varchar NOT NULL,
  "type_line" varchar NOT NULL,
  "rarity" varchar NOT NULL,
  "identified" bool NOT NULL,
  "item_level" tinyint NOT NULL,
  "forum_note" varchar,
  "currency_amount" float(24),
  "currency_name" varchar,
  "corrupted" bool,
  "delve" bool,
  "fractured" bool,
  "synthesized" bool,
  "replica" bool,
  "elder" bool,
  "shaper" bool,
  "searing" bool,
  "tangled" bool,
  "influences" jsonb,
  "is_relic" bool,
  "prefixes" tinyint,
  "suffixes" tinyint,
  "foil_variation" int,
  "inventory_id" varchar,
  "created_at" datetime,
  "updated_at" datetime,
  FOREIGN KEY (icon_url) REFERENCES Icon(icon_url) ON DELETE SET NULL,
  FOREIGN KEY (currency_name) REFERENCES Currency(currency_name) ON DELETE RESTRICT,
  FOREIGN KEY (stash_id) REFERENCES Stash(stash_id) ON DELETE CASCADE
);

CREATE TABLE "Transaction" (
  "transaction_id" serial PRIMARY KEY, -- Self generated
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


CREATE TABLE "Item_Categories" (
  "category_name" varchar PRIMARY KEY,
  "item_id" varchar PRIMARY KEY,
  FOREIGN KEY (category_name) REFERENCES Category(category_name) ON DELETE CASCADE,
  FOREIGN KEY (item_id) REFERENCES Item(item_id) ON DELETE CASCADE
);

CREATE TABLE "Item_Modifiers" (
  "modifier_id" varchar PRIMARY KEY,
  "item_id" varchar PRIMARY KEY
  FOREIGN KEY (modifier_id) REFERENCES Modifier(modifier_id) ON DELETE CASCADE,
  FOREIGN KEY (item_id) REFERENCES Item(item_id) ON DELETE CASCADE
);

CREATE TABLE "Category" (
  "category_name" varchar PRIMARY KEY, -- Field "extended" -> "category" and "subcategory" in Item POE API object
  "is_sub_category" bool
);

CREATE TABLE "Modifier" (
  "modifier_id" varchar PRIMARY KEY, -- Self generated with Modifier.effect for sensible uniqueness
  "effect" varchar NOT NULL,
  "implicit" bool NOT NULL,
  "explicit" bool NOT NULL,
  "delve" bool,
  "fractured" bool NOT NULL,
  "synthesized" bool NOT NULL,
  "corrupted" bool,
  "enchanted" bool NOT NULL,
  "veiled" bool NOT NULL,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "Modifier_Stats" (
  "modifier_id" varchar PRIMARY KEY,
  "stat_id" varchar PRIMARY KEY,
  "position" tinyint NOT NULL UNIQUE, -- If it's the first/second/third... number in the Modifier.effect text
  "stat_value" smallint, -- Value of the # in Modifier.effect text
  FOREIGN KEY (modifier_id) REFERENCES Modifier(modifier_id) ON DELETE CASCADE,
  FOREIGN KEY (stat_id) REFERENCES Stat(stat_id) ON DELETE CASCADE
);

CREATE TABLE "Stat" (
  "stat_id" varchar PRIMARY KEY, -- Generated with "local_" + "_" replaced for whitespace in Modifier.effect for sensible uniqueness
  "mininum_value" smallint,
  "maximum_value" smallint,
  "stat_tier" smallint, -- Tier 1 is highest tier 
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "Stash" (
  "stash_id" varchar PRIMARY KEY, -- Field "id" in PublicStashChange POE API object
  "account_name" varchar NOT NULL,
  "public" bool NOT NULL,
  "league" varchar NOT NULL,
  "created_at" datetime,
  "updated_at" datetime,
  FOREIGN KEY (account_name) REFERENCES Account(account_name) ON DELETE CASCADE,
);

CREATE TABLE "Account" (
  "account_name" varchar PRIMARY KEY,
  "is_banned" bool,
  "created_at" datetime,
  "updated_at" datetime
);

INSERT INTO Currency (currency_name, value_in_chaos, icon_url) VALUES ('Chaos Orb', 1, 'https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyRerollRare.png');

