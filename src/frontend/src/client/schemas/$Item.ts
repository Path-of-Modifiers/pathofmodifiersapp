/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Item = {
    properties: {
        gameItemId: {
            type: 'string',
            isRequired: true,
        },
        name: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        league: {
            type: 'string',
            isRequired: true,
        },
        baseType: {
            type: 'string',
            isRequired: true,
        },
        typeLine: {
            type: 'string',
            isRequired: true,
        },
        ilvl: {
            type: 'number',
            isRequired: true,
        },
        rarity: {
            type: 'string',
            isRequired: true,
        },
        identified: {
            type: 'boolean',
        },
        currencyAmount: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
        currencyId: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
        corrupted: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        delve: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        fractured: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        synthesised: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        replica: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        influences: {
            type: 'any-of',
            contains: [{
                type: 'Influences',
            }, {
                type: 'null',
            }],
        },
        searing: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        tangled: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        isRelic: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        prefixes: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
        suffixes: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
        foilVariation: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
        createdAt: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        itemId: {
            type: 'number',
            isRequired: true,
        },
    },
} as const;
