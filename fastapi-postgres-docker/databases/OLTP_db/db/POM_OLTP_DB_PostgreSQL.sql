CREATE TABLE "Currency" (
  "currencyName" varchar PRIMARY KEY,
  "valueInChaos" float NOT NULL,
  "iconUrl" varchar NOT NULL unique,
  "createdAt" datetime,
  "updatedAt" datetime
);

CREATE TABLE "Item" (
  "itemId" varchar PRIMARY KEY, 
  "stashId" varchar NOT NULL,
  "name" varchar,
  "iconUrl" varchar,
  "league" varchar NOT NULL,
  "typeLine" varchar NOT NULL,
  "baseType" varchar NOT NULL,
  "rarity" varchar NOT NULL,
  "identified" boolean NOT NULL,
  "itemLevel" smallint NOT NULL,
  "forumNote" varchar,
  "currencyAmount" float(24),
  "currencyName" varchar,
  "corrupted" boolean,
  "delve" boolean,
  "fractured" boolean,
  "synthesized" boolean,
  "replica" boolean,
  "elder" boolean,
  "shaper" boolean,
  "influences" jsonb,
  "searing" boolean,
  "tangled" boolean,
  "isrelic" boolean,
  "prefixes" smallint,
  "suffixes" smallint,
  "foilVariation" int,
  "inventoryId" varchar,
  "createdAt" datetime,
  "updatedAt" datetime,
  FOREIGN KEY (baseType) REFERENCES ItemBaseType(baseType) ON DELETE RESTRICT,
  FOREIGN KEY (currencyName) REFERENCES Currency(currencyName) ON DELETE RESTRICT,
  FOREIGN KEY (stashId) REFERENCES Stash(stashId) ON DELETE CASCADE
);

CREATE TABLE "Transaction" (
  "transactionId" serial PRIMARY KEY, 
  "itemId" varchar NOT NULL,
  "accountName" varchar NOT NULL,
  "currencyAmount" float(24) NOT NULL,
  "currencyName" varchar NOT NULL,
  "createdAt" datetime,
  "updatedAt" datetime,
  FOREIGN KEY (itemId) REFERENCES Item(itemId) ON DELETE CASCADE,
  FOREIGN KEY (accountName) REFERENCES Account(accountName) ON DELETE CASCADE,
  FOREIGN KEY (currencyName) REFERENCES Currency(currencyName) ON DELETE RESTRICT
);

CREATE TABLE "ItemBaseType" (
  "baseType" varchar PRIMARY KEY,
  "category" varchar NOT NULL unique,
  "subCategory" jsonb NOT NULL,
  "createdAt" datetime,
  "updatedAt" datetime
);

CREATE TABLE "ItemModifiers" (
  "modifierId" varchar PRIMARY KEY,
  "itemId" varchar PRIMARY KEY,
  FOREIGN KEY (modifierId) REFERENCES Modifier(modifierId) ON DELETE CASCADE,
  FOREIGN KEY (itemId) REFERENCES Item(itemId) ON DELETE CASCADE
);

CREATE TABLE "Modifier" (
  "modifierId" varchar PRIMARY KEY, 
  "effect" varchar NOT NULL,
  "implicit" boolean,
  "explicit" boolean,
  "delve" boolean,
  "fractured" boolean,
  "synthesized" boolean,
  "corrupted" boolean,
  "enchanted" boolean,
  "veiled" boolean,
  "createdAt" datetime,
  "updatedAt" datetime
);

CREATE TABLE "ModifierStats" (
  "modifierId" varchar PRIMARY KEY,
  "statId" varchar PRIMARY KEY,
  FOREIGN KEY (modifierId) REFERENCES Modifier(modifierId) ON DELETE CASCADE,
  FOREIGN KEY (statId) REFERENCES Stat(statId) ON DELETE CASCADE
);

CREATE TABLE "Stat" (
  "statId" varchar PRIMARY KEY, 
  "position" smallint NOT NULL PRIMARY KEY, 
  "statValue" smallint NOT NULL, 
  "mininumValue" smallint,
  "maximumValue" smallint,
  "statTier" smallint, 
  "createdAt" datetime,
  "updatedAt" datetime
);

CREATE TABLE "Stash" (
  "stashId" varchar PRIMARY KEY, 
  "accountName" varchar NOT NULL,
  "public" boolean NOT NULL,
  "league" varchar NOT NULL,
  "createdAt" datetime,
  "updatedAt" datetime,
  FOREIGN KEY (accountName) REFERENCES Account(accountName) ON DELETE CASCADE
);

CREATE TABLE "Account" (
  "accountName" varchar PRIMARY KEY,
  "isBanned" boolean,
  "createdAt" datetime,
  "updatedAt" datetime
);