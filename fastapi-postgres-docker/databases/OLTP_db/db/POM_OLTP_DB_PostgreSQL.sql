CREATE TABLE "Currency" (
  "currencyName" varchar,
  "valueInChaos" float NOT NULL,
  "iconUrl" varchar NOT NULL unique,
  "createdAt" datetime,
  "updatedAt" datetime,
  PRIMARY KEY (currencyName)
);

CREATE TABLE "Item" (
  "itemId" varchar, 
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
  "isRelic" boolean,
  "prefixes" smallint,
  "suffixes" smallint,
  "foilVariation" int,
  "inventoryId" varchar,
  "createdAt" datetime,
  "updatedAt" datetime,
  PRIMARY KEY (itemId),
  FOREIGN KEY (baseType) REFERENCES ItemBaseType(baseType) ON DELETE RESTRICT,
  FOREIGN KEY (currencyName) REFERENCES Currency(currencyName) ON DELETE RESTRICT,
  FOREIGN KEY (stashId) REFERENCES Stash(stashId) ON DELETE CASCADE
);

CREATE TABLE "Transaction" (
  "transactionId" serial, 
  "itemId" varchar NOT NULL,
  "accountName" varchar NOT NULL,
  "currencyAmount" float(24) NOT NULL,
  "currencyName" varchar NOT NULL,
  "createdAt" datetime,
  "updatedAt" datetime,
  PRIMARY KEY (transactionId),
  FOREIGN KEY (itemId) REFERENCES Item(itemId) ON DELETE CASCADE,
  FOREIGN KEY (accountName) REFERENCES Account(accountName) ON DELETE CASCADE,
  FOREIGN KEY (currencyName) REFERENCES Currency(currencyName) ON DELETE RESTRICT
);

CREATE TABLE "ItemBaseType" (
  "baseType" varchar NOT NULL,
  "category" varchar NOT NULL unique,
  "subCategory" varchar NOT NULL,
  "createdAt" datetime,
  "updatedAt" datetime,
  PRIMARY KEY (baseType)
);

CREATE TABLE "ItemModifier" (
  "itemId" varchar NOT NULL,
  "modifierId" varchar NOT NULL,
  "position" smallint NOT NULL,
  "range" float(24),
  PRIMARY KEY (modifierId, itemId, position),
  FOREIGN KEY (itemId) REFERENCES Item(itemId) ON DELETE CASCADE,
  FOREIGN KEY (position) REFERENCES Modifier(position) ON DELETE CASCADE,
  FOREIGN KEY (modifierId) REFERENCES Modifier(modifierId) ON DELETE CASCADE
);

CREATE TABLE "Modifier" (
  "modifierId" varchar, 
  "position" smallint,
  "minRoll" float(24),
  "maxRoll" float(24),
  "textRoll" varchar,
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
  "updatedAt" datetime,
  PRIMARY KEY (modifierId, position)
);

CREATE TABLE "Stash" (
  "stashId" varchar, 
  "accountName" varchar NOT NULL,
  "public" boolean NOT NULL,
  "league" varchar NOT NULL,
  "createdAt" datetime,
  "updatedAt" datetime,
  PRIMARY KEY (stashId),
  FOREIGN KEY (accountName) REFERENCES Account(accountName) ON DELETE CASCADE
);

CREATE TABLE "Account" (
  "accountName" varchar,
  "isBanned" boolean,
  "createdAt" datetime,
  "updatedAt" datetime,
  PRIMARY KEY (accountName)
);