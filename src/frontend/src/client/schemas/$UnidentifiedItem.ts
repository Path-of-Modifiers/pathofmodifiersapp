/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UnidentifiedItem = {
    properties: {
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
        itemBaseTypeId: {
            type: 'number',
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
        createdHoursSinceLaunch: {
            type: 'number',
            isRequired: true,
        },
        itemId: {
            type: 'number',
            isRequired: true,
        },
        nItems: {
            type: 'number',
            isRequired: true,
        },
        aggregated: {
            type: 'boolean',
            isRequired: true,
        },
    },
} as const;
