/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $TurnstileResponse = {
    properties: {
        success: {
            type: 'boolean',
            isRequired: true,
        },
        error_codes: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'string',
                },
            }, {
                type: 'null',
            }],
        },
        challenge_ts: {
            type: 'string',
            isRequired: true,
        },
        hostname: {
            type: 'string',
            isRequired: true,
        },
        action: {
            type: 'string',
            isRequired: true,
        },
        cdata: {
            type: 'string',
            isRequired: true,
        },
        metadata: {
            type: 'dictionary',
            contains: {
                properties: {
                },
            },
            isRequired: true,
        },
    },
} as const;
