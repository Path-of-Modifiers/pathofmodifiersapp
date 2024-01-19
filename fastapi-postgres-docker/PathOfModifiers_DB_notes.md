# Notes about Path of Modifiers DB


## Fields of interest
### PublicStashChange 

| Key               | Value Type    | Extra Information                                   | Useful | COMMENT    |
|:----------------- |:------------- |:--------------------------------------------------- | ------ | --- |
| id                | string        | a unique 64 digit hexadecimal string                |    YES    |     |
| public            | bool          | if false then optional properties will be null      |    YES    |     |
| <del>accountName       | ?string       |                                                     |    NO    |     |
| <del>stash             | ?string       | the name of the stash                               |    NO    |     |
| <del>lastCharacterName | ?string       | not included by default. Requires extra permissions |   NO     |     |
| <del>stashType         | string        |                                                     |    NO    |     |
| <del>league            | ?string       | the league's name                                   |   YES     |     |
|<del> items             | array of Item |                                                     |   YES     |     |


### Item


| Key                   | Value Type                 | Extra Information                                                            | Useful | COMMENT    |
|:--------------------- |:-------------------------- |:---------------------------------------------------------------------------- | ------ | --- |
| <del>verified         | bool                       |                                                                              | NO     |     |
| <del>w                | uint                       |                                                                              | NO     |     |
| <del>h                | uint                       |                                                                              | NO     |     |
| icon                  | string                     |                                                                              | YES    |     |
| <del>support          | ?bool                      | always true if present                                                       | NO     |     |
| <del>stackSize        | ?int                       |                                                                              | NO     |     |
| <del>maxStackSize     | ?int                       |                                                                              | NO     |     |
| <del>stackSizeText    | ?string                    |                                                                              | NO     |     |
| league                | ?string                    |                                                                              | YES    |     |
| id                    | ?string                    | a unique 64 digit hexadecimal string                                         | YES    |     |
| influences            | ?object                    |                                                                              | MAYBE  |     |
| elder                 | ?bool                      | always true if present                                                       | MAYBE  |     |
| shaper                | ?bool                      | always true if present                                                       | MAYBE  |     |
| searing               | ?bool                      | always true if present                                                       | MAYBE  |     |
| tangled               | ?bool                      | always true if present                                                       | MAYBE  |     |
| <del>abyssJewel       | ?bool                      | always true if present                                                       | NO     |     |
| delve                 | ?bool                      | always true if present                                                       | YES    |     |
| fractured             | ?bool                      | always true if present                                                       | YES    |     |
| synthesised           | ?bool                      | always true if present                                                       | YES    |     |
| <del>sockets          | ?array of ItemSocket       |                                                                              | NO     |     |
| <del>socketedItems    | ?array of Item             |                                                                              | NO     |     |
| name                  | string                     |                                                                              | YES    |     |
| typeLine              | string                     |                                                                              | YES    |     |
| baseType              | string                     |                                                                              | YES    |     |
| rarity                | ?string                    | Normal, Magic, Rare, or Unique                                               | YES    |     |
| identified            | bool                       |                                                                              | YES    |     |
| itemLevel             | ?int                       |                                                                              | YES    |     |
| ilvl                  | int                        | deprecated                                                                   | YES    |  Need to replace with `itemLevel`   |
| note                  | ?string                    | user-generated text                                                          | YES    |     |
| forum_note            | ?string                    | user-generated text                                                          | YES    |     |
| <del>lockedToCharacter     | ?bool                      | always true if present                                                       |  NO      |     |
| <del>lockedToAccount       | ?bool                      | always true if present                                                       |   NO     |     |
| <del>duplicated            | ?bool                      | always true if present                                                       |    NO    |     |
| split                 | ?bool                      | always true if present                                                       |   MAYBE     |     |
| corrupted             | ?bool                      | always true if present                                                       |    YES    |     |
| unmodifiable          | ?bool                      | always true if present                                                       |   NO     |     |
| <del>cisRaceReward         | ?bool                      | always true if present                                                       |    NO    |     |
| <del>seaRaceReward         | ?bool                      | always true if present                                                       |   NO     |     |
| <del>thRaceReward          | ?bool                      | always true if present                                                       |   NO     |     |
| properties            | ?array of ItemProperty     |                                                                              |    MAYBE    |     |
| notableProperties     | ?array of ItemProperty     |                                                                              |    MAYBE    |     |
| requirements          | ?array of ItemProperty     |                                                                              |   MAYBE     |     |
| additionalProperties  | ?array of ItemProperty     |                                                                              |    MAYBE    |     |
| <del>nextLevelRequirements | ?array of ItemProperty     |                                                                              |   NO     |     |
| <del>talismanTier          | ?int                       |                                                                              |    NO    |     |
| rewards               | ?array of object           |                                                                              |    MAYBE    |     |
| ↳ label               | string                     |                                                                              |   MAYBE     |     |
| ↳ rewards             | dictionary of int          | the key is a string representing the type of reward. The value is the amount |    MAYBE    |     |
| <del>secDescrText          | ?string                    |                                                                              |   NO     |     |
| <del>secDescrText          | ?string                    |                                                                              |   NO     |     |
| <del>utilityMods           | ?array of string           |                                                                              |   NO     |     |
| <del>logbookMods           | ?array of object           |                                                                              |   NO     |     |
| <del>↳ name                | string                     | area name                                                                    |     NO   |     |
| <del>↳ faction             | object                     |                                                                              |    NO    |     |
| <del>↳ id                  | string                     | Faction1, Faction2, Faction3, or Faction4                                    |    NO    |     |
| <del>↳ name                | string                     |                                                                              |    NO    |     |
| <del>↳ mods                | array of string            |                                                                              |   NO     |     |
| enchantMods           | ?array of string           |                                                                              |    YES    |     |
| <del>scourgeMods           | ?array of string           |                                                                              |    NO    |     |
| implicitMods          | ?array of string           |                                                                              |        |     |
| <del>ultimatumMods         | ?array of object           |                                                                              |    NO    |     |
| <del>↳ type                | string                     | text used to display ultimatum icons                                         |   NO     |     |
| <del>↳ tier                | uint                       |                                                                              |   NO     |     |
| explicitMods          | ?array of string           |                                                                              |    YES    |     |
| <del>craftedMods           | ?array of string           |                                                                              |  NO      |     |
| fracturedMods         | ?array of string           |                                                                              |  YES      |     |
| <del>crucibleMods          | ?array of string           | only allocated mods are included                                             |    NO    |     |
| <del>cosmeticMods          | ?array of string           |                                                                              |    NO    |     |
| veiledMods            | ?array of string           | random video identifier                                                      |    MAYBE    |     |
| veiled                | ?bool                      | always true if present                                                       |   MAYBE     |     |
| <del>descrText             | ?string                    |                                                                              |   NO     |     |
| <del>flavourText           | ?array of string           |                                                                              |   NO     |     |
| <del>flavourTextParsed     | ?array of string or object |                                                                              |  NO      |     |
| <del>flavourTextNote       | ?string                    | user-generated text                                                          |   NO     |     |
| <del>prophecyText          | ?string                    |                                                                              |    NO    |     |
| isRelic               | ?bool                      | always true if present                                                       |   MAYBE     |     |
| foilVariation         | ?int                       |                                                                              |   YES     |     |
| replica               | ?bool                      | always true if present                                                       |  MAYBE      |     |
| <del>foreseeing            | ?bool                      | always true if present                                                       |   NO     |     |
| <del>incubatedItem         | ?object                    |                                                                              |   NO     |     |
| <del>↳ name                | string                     |                                                                              |  NO      |     |
| <del>↳ level               | uint                       | monster level required to progress                                           |   NO     |     |
| <del>↳ progress            | uint                       |                                                                              |    NO    |     |
| <del>↳ total               | uint                       |                                                                              |   NO     |     |
|<del>scourged              | ?object                    |                                                                              |    NO    |     |
| <del>↳ tier                | uint                       | 1-3 for items, 1-10 for maps                                                 |   NO     |     |
|<del> ↳ level               | ?uint                      | monster level required to progress                                           |   NO     |     |
| <del>↳ progress            | ?uint                      |                                                                              |   NO     |     |
|<del> ↳ total               | ?uint                      |                                                                              |   NO     |     |
| <del>crucible              | ?object                    |                                                                              |   NO     |     |
| <del>↳ layout              | string                     | URL to an image of the tree layout                                           |  NO      |     |
| <del>↳ nodes               | dictionary of CrucibleNode | the key is the string value of the node index                                |   NO     |     |
|<del> ruthless              | ?bool                      | always true if present                                                       |   NO     |     |
|<del> frameType             | ?uint as FrameType         |                                                                              |   NO     |     |
|<del> artFilename           | ?string                    |                                                                              |   NO     |     |
|<del> hybrid                | ?object                    |                                                                              |   NO     |     |
|<del> ↳ isVaalGem           | ?bool                      |                                                                              |    NO    |     |
| <del>↳ baseTypeName        | string                     |                                                                              |    NO    |     |
|<del> ↳ properties          | ?array of ItemProperty     |                                                                              |   NO     |     |
|<del> ↳ explicitMods        | ?array of string           |                                          <del> ↳ secDescrText        | ?string                    |                                                                              |   NO     |     |
| extended              | ?object                    | only present in the Public Stash API                                         |    YES    |     |
| ↳ category            | ?string                    |                                                                              |   YES     |     |
| ↳ subcategories       | ?array of string           |                                                                              |    YES    |     |
| ↳ prefixes            | ?uint                      |                                                                              |   YES     |     |
| ↳ suffixes            | ?uint                      |                                                                              |   YES     |     |
|<del> x                     | ?uint                      |                                                                              |   NO     |     |
|<del> y                     | ?uint                      |                                                                              |    NO    |     |
| inventoryId           | ?string                    |                                                                              |    YES    |     |
|<del> socket                | ?uint                      |                                                                              |    NO    |     |
|<del> colour                | ?string                    |                                                                              |   NO     |     |
