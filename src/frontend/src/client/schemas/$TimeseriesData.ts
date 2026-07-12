/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $TimeseriesData = {
    properties: {
        name: {
            type: 'number',
            isRequired: true,
        },
        data: {
            type: 'array',
            contains: {
                type: 'Datum',
            },
            isRequired: true,
        },
        confidenceRating: {
            type: 'Enum',
            isRequired: true,
        },
    },
} as const;
