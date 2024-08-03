/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $TurnstyleResponse = {
    properties: {
        success: {
            type: 'boolean',
            isRequired: true,
        },
        challenge_ts: {
            type: 'string',
            isRequired: true,
        },
        hostname: {
            type: 'string',
            isRequired: true,
        },
        error_codes: {
            type: 'array',
            contains: {
                type: 'string',
            },
            isRequired: true,
        },
    },
} as const;
