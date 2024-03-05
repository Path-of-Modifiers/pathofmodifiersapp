# API documentation for POM


## /account

### [GET] "/account/{accountName}"  Get Account

Retrieves the POE account user by mapping with key and value for "accountName". 

Always returns one account.

![get_account](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/a2a7108a-8da6-4a28-a4a1-a2244edb6e45)

### [GET] "/account/" Get All Accounts

Get all accounts.

Returns a list of all accounts.

![get_all_accounts](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/21d1145c-6cb9-4d7b-838a-6398a888b0bf)

### [POST] "/account/" Create Account

Create one or a list of accounts.

Returns the created account or list of accounts.

![create_account](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/83de3d02-177d-432d-90c1-8756df2ced87)


### [PUT] "/account/{accountName}" Update Account

Update an account by key and value for "accountName".

Returns the updated account.

![update_account](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/e3a277d9-da25-4952-a0f3-5814f2dca61a)


### [DELETE] "/account/{accountName}" Delete Account

Delete an account by key and value "accountName".

Returns a message indicating the account was deleted.
Always deletes one account.

![delete_account](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/5caaab74-ce9f-4384-b1d6-c6251c6a05bf)



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

Returns the updated item modifier.

![update_item_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/f72a1144-efc1-4080-8d60-414e50d6e624)

### [DELETE] "/itemModifier/{itemId}" Delete Item Modifier

Delete an item modifier by key and value for 
"itemId", optional "modifierId" and optional "position".

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

Returns the updated modifier.

![update_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/e7e972f8-b78c-499c-9f96-14dba050f774)


### [DELETE] "/modifier/{modifierId}" Delete Modifier

Delete a modifier by key and value for "modifierId" 
and optional "position".

Returns a message that the modifier was deleted.

![delete_modifier](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/e906d3ef-d7ae-4154-90a2-c1d047262422)



## /stash

### [GET] "/stash/{stashId}"  Get Stash

Get stash by key and value for "stashId".

Always returns one stash.

![get_stash](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/d5e8657e-d05c-4e68-8aaa-5336a8334c75)

### [GET] "/stash/" Get All Stashes

Get all stashes.

Returns a list of all stashes.

![get_all_stashes](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/77e3f60e-0fd1-4a22-aaa1-85b3c7c4f40b)

### [POST] "/stash/" Create Stash

Create one or a list of new stashes.

Returns the created stash or list of stashes.

![create_stash](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/d5985a2a-9cb0-45e4-a0ad-ad6067031a9d)


### [PUT] "/stash/{stashId}" Update Stash

Update a stash by key and value for "stashId".

Returns the updated stash.

![update_stash](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/817d289c-0d64-47d3-accc-1abc8ba9b1d6)


### [DELETE] "/stash/{stashId}" Delete Stash

Delete a stash by key and value for "stashId".

Returns a message that the stash was deleted successfully.
Always deletes one stash.

![delete_stash](https://github.com/Ivareh/pathofmodifiersapp/assets/69577035/ad38bd4d-6edf-47dc-9cc6-904e261b868c)