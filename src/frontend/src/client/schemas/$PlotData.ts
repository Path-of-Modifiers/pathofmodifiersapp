/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $PlotData = {
    properties: {
        mostCommonCurrencyUsed: {
            type: 'string',
            isRequired: true,
        },
        data: {
            type: 'array',
            contains: {
                type: 'TimeseriesData',
            },
            isRequired: true,
        },
    },
} as const;
