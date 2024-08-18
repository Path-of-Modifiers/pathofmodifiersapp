/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $PlotData = {
    properties: {
        valueInChaos: {
            type: 'array',
            contains: {
                type: 'number',
            },
            isRequired: true,
        },
        timeStamp: {
            type: 'array',
            contains: {
                type: 'string',
                format: 'date-time',
            },
            isRequired: true,
        },
        valueInMostCommonCurrencyUsed: {
            type: 'array',
            contains: {
                type: 'number',
            },
            isRequired: true,
        },
        mostCommonCurrencyUsed: {
            type: 'string',
            isRequired: true,
        },
    },
} as const;
