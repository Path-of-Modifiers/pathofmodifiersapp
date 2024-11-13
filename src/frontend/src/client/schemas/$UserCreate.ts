/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserCreate = {
    properties: {
        username: {
            type: 'string',
            isRequired: true,
            maxLength: 30,
            pattern: '^[\\p{L}\\p{N}_]+$',
        },
        email: {
            type: 'string',
            isRequired: true,
            format: 'email',
        },
        isActive: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        isSuperuser: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        rateLimitTier: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
        isBanned: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        password: {
            type: 'string',
            isRequired: true,
            minLength: 8,
        },
    },
} as const;
