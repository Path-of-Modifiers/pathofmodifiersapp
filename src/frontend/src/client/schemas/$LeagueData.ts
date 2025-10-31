/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $LeagueData = {
    properties: {
        league: {
            type: 'string',
            isRequired: true,
        },
        linkedPrices: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'LinkedPrices',
                },
            }, {
                type: 'null',
            }],
        },
        unlinkedPrices: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'Datum',
                },
            }, {
                type: 'null',
            }],
        },
    },
} as const;
