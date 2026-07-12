/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $LeagueCreate = {
    properties: {
        name: {
            type: 'string',
            isRequired: true,
        },
        validFrom: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        validTo: {
            type: 'any-of',
            contains: [{
                type: 'string',
                format: 'date-time',
            }, {
                type: 'null',
            }],
        },
    },
} as const;
