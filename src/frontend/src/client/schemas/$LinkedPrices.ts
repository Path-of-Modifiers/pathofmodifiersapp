/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $LinkedPrices = {
    properties: {
        gameItemId: {
            type: 'string',
            isRequired: true,
        },
        data: {
            type: 'array',
            contains: {
                type: 'Datum',
            },
            isRequired: true,
        },
    },
} as const;
