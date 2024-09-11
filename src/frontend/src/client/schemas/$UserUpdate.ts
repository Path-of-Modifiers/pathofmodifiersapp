/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserUpdate = {
    properties: {
        username: {
            type: 'any-of',
            contains: [{
                type: 'string',
                pattern: '^[\\p{L}\\p{N}_]+$',
            }, {
                type: 'null',
            }],
        },
        email: {
            type: 'any-of',
            contains: [{
                type: 'string',
                format: 'email',
            }, {
                type: 'null',
            }],
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
            type: 'any-of',
            contains: [{
                type: 'string',
                minLength: 8,
            }, {
                type: 'null',
            }],
        },
    },
} as const;
