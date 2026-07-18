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
        leagueId: {
            type: 'number',
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
        nItems: {
            type: 'number',
        },
        aggregated: {
            type: 'boolean',
        },
        createdHoursSinceLaunch: {
            type: 'number',
            isRequired: true,
        },
        itemId: {
            type: 'number',
            isRequired: true,
        },
    },
} as const;
