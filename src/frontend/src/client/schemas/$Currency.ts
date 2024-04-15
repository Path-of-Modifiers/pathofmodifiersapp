/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Currency = {
    properties: {
        tradeName: {
            type: 'string',
            isRequired: true,
        },
        valueInChaos: {
            type: 'number',
            isRequired: true,
        },
        iconUrl: {
            type: 'string',
            isRequired: true,
        },
        createdAt: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        currencyId: {
            type: 'number',
            isRequired: true,
        },
    },
} as const;
