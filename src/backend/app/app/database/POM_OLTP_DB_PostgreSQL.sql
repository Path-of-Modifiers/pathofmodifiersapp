CREATE TABLE "Currency" (
  "currencyName" varchar(50) NOT NULL,
  "valueInChaos" numeric(10,2) NOT NULL,
  "iconUrl" varchar(300) NOT NULL UNIQUE,
  "createdAt" datetime NOT NULL,
  "updatedAt" datetime NOT NULL,
  PRIMARY KEY (currencyName)
);

CREATE TABLE "ItemBaseType" (
  "baseType" varchar(40) NOT NULL,
  "category" varchar(40) NOT NULL UNIQUE,
  "subCategory" varchar(40),
  "createdAt" datetime NOT NULL,
  "updatedAt" datetime NOT NULL,
  PRIMARY KEY (baseType),
  UNIQUE (category, subCategory)
);

CREATE TABLE "Item" (
  "itemId" varchar(200), 
  "stashId" varchar(200) NOT NULL,
  "name" varchar(80),
  "iconUrl" varchar(400),
  "league" varchar(20) NOT NULL,
  "typeLine" varchar(40) NOT NULL,
  "baseType" integer NOT NULL,
  "rarity" varchar(20) NOT NULL,
  "identified" boolean NOT NULL,
  "itemLevel" smallint NOT NULL,
  "forumNote" varchar(40),
  "currencyAmount" numeric(12, 2),
  "currencyName" varchar(50) NOT NULL,
  "corrupted" boolean,
  "delve" boolean,
  "fractured" boolean,
  "synthesized" boolean,
  "replica" boolean,
  "influences" jsonb,
  "searing" boolean,
  "tangled" boolean,
  "isRelic" boolean,
  "prefixes" smallint,
  "suffixes" smallint,
  "foilVariation" smallint,
  "createdAt" datetime NOT NULL,
  "updatedAt" datetime NOT NULL,
  PRIMARY KEY (itemId),
  FOREIGN KEY (baseType) REFERENCES ItemBaseType(baseType) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (currencyName) REFERENCES Currency(currencyName) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (stashId) REFERENCES Stash(stashId) ON DELETE CASCADE
);

CREATE TABLE "Modifier" (
  "modifierId" serial, 
  "effect" varchar(200) NOT NULL,
  "position" smallint NOT NULL,
  "static" boolean,
  "minRoll" numeric(10, 2),
  "maxRoll" numeric(10, 2),
  "textRoll" varchar(30),
  "implicit" boolean,
  "explicit" boolean,
  "delve" boolean,
  "fractured" boolean,
  "synthesized" boolean,
  "corrupted" boolean,
  "enchanted" boolean,
  "veiled" boolean,
  "createdAt" datetime NOT NULL,
  "updatedAt" datetime NOT NULL,
  PRIMARY KEY (modifierId),
  UNIQUE (position, effect)
);

CREATE TABLE "ItemModifier" (
  "itemId" varchar(200) NOT NULL,
  "modifierId" integer NOT NULL,
  "position" smallint NOT NULL,
  "range" numeric(10, 2),
  PRIMARY KEY (itemId, modifierId, position),
  FOREIGN KEY (itemId) REFERENCES Item(itemId) ON DELETE CASCADE,
  FOREIGN KEY (modifierId, position) REFERENCES Modifier(modifierId, position) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "Account" (
  "accountName" varchar(40),
  "isBanned" boolean,
  "createdAt" datetime NOT NULL,
  "updatedAt" datetime NOT NULL,
  PRIMARY KEY (accountName)
);

CREATE TABLE "Stash" (
  "stashId" varchar(200), 
  "accountName" varchar(40) NOT NULL,
  "public" boolean NOT NULL,
  "league" varchar(20) NOT NULL,
  "createdAt" datetime NOT NULL,
  "updatedAt" datetime NOT NULL,
  PRIMARY KEY (stashId),
  FOREIGN KEY (accountName) REFERENCES Account(accountName) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "Transaction" (
  "transactionId" serial, 
  "itemId" varchar(200) NOT NULL,
  "accountName" varchar(40) NOT NULL,
  "currencyAmount" numeric(12,2) NOT NULL,
  "currencyName" varchar(40) NOT NULL,
  "createdAt" datetime NOT NULL,
  "updatedAt" datetime NOT NULL,
  PRIMARY KEY (transactionId),
  FOREIGN KEY (itemId) REFERENCES Item(itemId) ON DELETE CASCADE,
  FOREIGN KEY (accountName) REFERENCES Account(accountName) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (currencyName) REFERENCES Currency(currencyName) ON DELETE RESTRICT ON UPDATE CASCADE
);
