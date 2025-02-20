# Currently outdated. Check out $DOMAIN/docs for updated contents

## Table of contents
- [API documentation for POM](#api-documentation-for-pom)
  - [/currency](#currency)
    - [\[GET\] "/currency/{currencyId}" Get Currency](#get-currencycurrencyid-get-currency)
    - [\[GET\] "/currency/" Get All Currencies](#get-currency-get-all-currencies)
    - [\[POST\] "/currency/" Create Currency](#post-currency-create-currency)
    - [\[PUT\] "/currency/{currencyId}" Update Currency](#put-currencycurrencyid-update-currency)
    - [\[DELETE\] "/currency/{currencyId}" Delete Currency](#delete-currencycurrencyid-delete-currency)
  - [/itemBaseType](#itembasetype)
    - [\[GET\] "/itemBaseType/{baseType}" Get Item Base Type](#get-itembasetypebasetype-get-item-base-type)
    - [\[GET\] "/itemBaseType/" Get All Item Base Types](#get-itembasetype-get-all-item-base-types)
    - [\[POST\] "/itemBaseType/" Create Item Base Type](#post-itembasetype-create-item-base-type)
    - [\[PUT\] "/itemBaseType/{baseType}" Update Item Base Type](#put-itembasetypebasetype-update-item-base-type)
    - [\[DELETE\] "/itemBaseType/{baseType}" Delete Item Base Type](#delete-itembasetypebasetype-delete-item-base-type)
  - [/itemModifier](#itemmodifier)
    - [\[GET\] "/itemModifier/{itemId}" Get Item Modifier](#get-itemmodifieritemid-get-item-modifier)
    - [\[GET\] "/itemModifier/" Get All Item Modifiers](#get-itemmodifier-get-all-item-modifiers)
    - [\[POST\] "/itemModifier/" Create Item Modifier](#post-itemmodifier-create-item-modifier)
    - [\[PUT\] "/itemModifier/{itemId}" Update Item Modifier](#put-itemmodifieritemid-update-item-modifier)
    - [\[DELETE\] "/itemModifier/{itemId}" Delete Item Modifier](#delete-itemmodifieritemid-delete-item-modifier)
  - [/item](#item)
    - [\[GET\] "/item/{itemId}"  Get Item](#get-itemitemid--get-item)
    - [\[GET\] "/item/" Get All Items](#get-item-get-all-items)
    - [\[POST\] "/item/" Create Item](#post-item-create-item)
    - [\[PUT\] "/item/{itemId}" Update Item](#put-itemitemid-update-item)
    - [\[DELETE\] "/item/{itemId}" Delete Item](#delete-itemitemid-delete-item)
  - [/modifier](#modifier)
    - [\[GET\] "/modifier/{modifierId}"  Get Modifier](#get-modifiermodifierid--get-modifier)
    - [\[GET\] "/modifier/" Get All Modifiers](#get-modifier-get-all-modifiers)
    - [\[POST\] "/modifier/" Create Modifier](#post-modifier-create-modifier)
    - [\[PUT\] "/modifier/{modifierId}" Update Modifier](#put-modifiermodifierid-update-modifier)
    - [\[DELETE\] "/modifier/{modifierId}" Delete Modifier](#delete-modifiermodifierid-delete-modifier)

# API documentation for POM

This section covers the API functions for version 1 in the POM app.

Each function serves one of five basic operations: retrieving specific data ``Get X``, retrieving all data ``Get All X``, creating data ``Create X``, updating data ``Update X``, and deleting data ``Delete X``.

The ``Get X`` function retrieves an object by mapping to its primary key. Some primary key attributes are essential and can't be null, while others in the query can be nullable. For ``Get X``, if any or all of the non-essential attributes are null, the query fetches all objects with non-null values for the primary key. It's worth noting that this feature is currently limited to ``Get X`` and isn't available for ``Update X`` and ``Delete X``. However, these capabilities are planned for future releases.


## /currency

### [GET] "/currency/{currencyId}" Get Currency

Get currency by key and value for "currencyId".

Always returns one currency.

![get_currency](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/58422369-bc4c-4b25-ac14-7c90a21b8a10)

### [GET] "/currency/" Get All Currencies

Get all currencies.

Returns a list of all currencies.

![get_all_currencies](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/d7d7b131-2631-4d2e-ae10-aafa0e430f82)

### [POST] "/currency/" Create Currency

Create one or a list of currencies.

Returns the created currency or list of currencies.

![create_currency](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/c0daccb6-97e5-4f35-9954-6ff287ac3fce)


### [PUT] "/currency/{currencyId}" Update Currency

Update a currency by key and value for "currencyId".

Returns the updated currency.

![update_currency](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/66822fa2-9325-42e2-b2ea-a1103f833fad)


### [DELETE] "/currency/{currencyId}" Delete Currency

Delete a currency by key and value for "currencyId".

Returns a message indicating the currency was deleted.

Always deletes one currency.

![delete_currency](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/1b84d3bf-7bdd-43a5-be06-2cd57149b72b)





## /itemBaseType

### [GET] "/itemBaseType/{baseType}" Get Item Base Type

Get item base type by key and value for "baseType".

Always returns one item base type.

![get_item_base_type](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/0867c743-bc6e-4622-b95b-2ac225b91352)

### [GET] "/itemBaseType/" Get All Item Base Types

Get all item base types.

Returns a list of all item base types.

![get_all_item_base_types](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/f8e8e65b-1041-40b9-9b8f-97fd1087b0a1)

### [POST] "/itemBaseType/" Create Item Base Type

Create one or a list of new item base types.

Returns the created item base type or list of item base types.

![create_item_base_type](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/04fb935e-ee30-4def-9dfa-996b432da00e)


### [PUT] "/itemBaseType/{baseType}" Update Item Base Type

Update an item base type by key and value for "baseType".

Returns the updated item base type.

![update_item_base_type](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/8c4b78bc-aaf0-47b0-a182-5e68bfe4d2d4)


### [DELETE] "/itemBaseType/{baseType}" Delete Item Base Type

Delete an item base type by key and value for "baseType".

Returns a message that the item base type was deleted successfully.

Always deletes one item base type.

![delete_item_base_type](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/315593bd-694c-4bea-9249-f2ed29bca0ce)



## /itemModifier

### [GET] "/itemModifier/{itemId}" Get Item Modifier

Get item modifier or list of item modifiers by key and
value for "itemId", optional "modifierId" and optional "position".

Dominant key is "itemId".

Returns one or a list of item modifiers.

![get_item_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/2eca9b4f-af3b-4b8b-bde5-ada32c338348)

### [GET] "/itemModifier/" Get All Item Modifiers

Get all item modifiers.

Returns a list of all item modifiers.

![get_all_item_modifiers](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/c378172c-6195-42eb-ab94-6828302454ca)

### [POST] "/itemModifier/" Create Item Modifier

Create one or a list item modifiers.

Returns the created item modifier or list of item modifiers.

![create_item_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/4f922a54-8545-4894-a21c-f88a4910f3bd)

### [PUT] "/itemModifier/{itemId}" Update Item Modifier

Update an item modifier by key and value for
"itemId", optional "modifierId" and optional "position".

Dominant key is "itemId".

Returns the updated item modifier.

![update_item_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/f72a1144-efc1-4080-8d60-414e50d6e624)

### [DELETE] "/itemModifier/{itemId}" Delete Item Modifier

Delete an item modifier by key and value for
"itemId", optional "modifierId" and optional "position".

Dominant key is "itemId".

Returns a message that the item modifier was deleted successfully.

Always deletes one item modifier.

![delete_item_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/a9c951d8-7aa6-4b81-b53f-e6904ae3a807)




## /item

### [GET] "/item/{itemId}"  Get Item

Get item by key and value for "itemId".

Always returns one item.

![get_item](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/08588a4b-cddc-4aaf-86ea-d0c8f0d48c78)

### [GET] "/item/" Get All Items

Get all items.

Returns a list of all items.

![get_all_items](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/b450097f-b75c-4e7a-9f10-62a23ff9573b)

### [POST] "/item/" Create Item

Create one or a list of new items.

Returns the created item or list of items.

![create_item](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/42404020-3e8d-454d-88c8-06e3cc07b88a)


### [PUT] "/item/{itemId}" Update Item

Update an item by key and value for "itemId".

Returns the updated item.

![update_item](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/54ca0201-a0eb-4dad-86c4-f57eefe01321)


### [DELETE] "/item/{itemId}" Delete Item

Delete an item by key and value for "itemId".

Returns a message indicating the item was deleted.

Always deletes one item.

![delete_item](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/974f7267-b31b-45ab-88e4-de37fc90d856)




## /modifier

### [GET] "/modifier/{modifierId}"  Get Modifier

Get modifier or list of modifiers by key and
value for "modifierId" and optional "position"

Dominant key is "modifierId".

Returns one or a list of modifiers.

![get_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/73a009ee-cef7-450a-bdae-af8264f79a99)

### [GET] "/modifier/" Get All Modifiers

Get all modifiers.

Returns a list of all modifiers.

![get_all_modifiers](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/1de82b32-0673-4cd7-80a4-86e6f15a30e5)

### [POST] "/modifier/" Create Modifier

Create one or a list of new modifiers.

Returns the created modifier or list of modifiers.

![create_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/421d446c-7657-4877-b3b8-f644adc1ed78)


### [PUT] "/modifier/{modifierId}" Update Modifier

Update a modifier by key and value for "modifierId" and "position".

Dominant key is "modifierId".

Returns the updated modifier.

![update_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/e7e972f8-b78c-499c-9f96-14dba050f774)


### [DELETE] "/modifier/{modifierId}" Delete Modifier

Delete a modifier by key and value for "modifierId"
and optional "position".

Dominant key is "modifierId".

Returns a message that the modifier was deleted.

Always deletes one modifier.

![delete_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/e906d3ef-d7ae-4154-90a2-c1d047262422)


