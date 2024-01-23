CREATE TABLE "Currency" (
  "currency_name" varchar PRIMARY KEY,
  "value_in_chaos" int NOT NULL,
  "icon_url" varchar NOT NULL,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "Item" (
  "item_id" varchar PRIMARY KEY,
  "name" varchar,
  "icon_url" varchar,
  "base_type" varchar NOT NULL,
  "type_line" varchar NOT NULL,
  "rarity" varchar NOT NULL,
  "identified" bool NOT NULL,
  "item_level" int,
  "forum_note" varchar NOT NULL,
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
  "foil_variation" int,
  "inventory_id" varchar,
  "created_at" datetime,
  "updated_at" datetime,
  FOREIGN KEY (icon_url) REFERENCES Icon(icon_url) ON DELETE SET NULL,
  FOREIGN KEY (currency_name) REFERENCES Currency(currency_name) ON DELETE RESTRICT
);

CREATE TABLE "Transaction" (
  "transaction_id" serial PRIMARY KEY,
  "item_id" varchar NOT NULL,
  "account_name" varchar NOT NULL,
  "currency_amount" int NOT NULL,
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
  "item_id" varchar PRIMARY KEY,
  FOREIGN KEY (modifier_id) REFERENCES Modifier(modifier_id) ON DELETE CASCADE,
  FOREIGN KEY (item_id) REFERENCES Item(item_id) ON DELETE CASCADE
);

CREATE TABLE "Icon" (
  "icon_url" varchar PRIMARY KEY,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "Category" (
  "category_name" varchar PRIMARY KEY,
  "is_sub_category" bool
);

CREATE TABLE "Modifier" (
  "modifier_id" varchar PRIMARY KEY, -- Generated with Modifier.effect for sensible uniqueness 
  "effect" varchar NOT NULL,
  "implicit" bool NOT NULL,
  "explicit" bool NOT NULL,
  "delve" bool,
  "fractured" bool NOT NULL,
  "synthesized" bool,
  "corrupted" bool,
  "enchanted" bool NOT NULL,
  "veiled" bool NOT NULL,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "Stash_Items" (
  "stash_id" varchar PRIMARY KEY,
  "item_id" varchar PRIMARY KEY,
  FOREIGN KEY (stash_id) REFERENCES Stash(stash_id) ON DELETE CASCADE,
  FOREIGN KEY (item_id) REFERENCES Item(item_id) ON DELETE CASCADE
);

CREATE TABLE "Stash" (
  "stash_id" varchar PRIMARY KEY,
  "account_name" varchar NOT NULL,
  "public" bool NOT NULL,
  "league" varchar NOT NULL,
  "created_at" datetime,
  "updated_at" datetime,
  FOREIGN KEY (account_name) REFERENCES Account(account_name) ON DELETE CASCADE,
  FOREIGN KEY (league) REFERENCES League(league_name) ON DELETE CASCADE
);

CREATE TABLE "Account" (
  "account_name" varchar PRIMARY KEY,
  "is_banned" bool,
  "created_at" datetime
);

CREATE TABLE "League" (
  "league_name" varchar PRIMARY KEY,
  "created_at" datetime
);

