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
            type: 'array',
            contains: {
                type: 'LinkedPrices',
            },
            isRequired: true,
        },
        unlinkedPrices: {
            type: 'array',
            contains: {
                type: 'Datum',
            },
            isRequired: true,
        },
    },
} as const;
