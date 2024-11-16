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
        hoursSinceLaunch: {
            type: 'array',
            contains: {
                type: 'number',
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
        confidence: {
            type: 'array',
            contains: {
                type: 'Enum',
            },
            isRequired: true,
        },
        confidenceRating: {
            type: 'Enum',
            isRequired: true,
        },
        mostCommonCurrencyUsed: {
            type: 'string',
            isRequired: true,
        },
    },
} as const;
