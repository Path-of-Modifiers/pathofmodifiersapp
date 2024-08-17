/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserUpdate = {
    properties: {
        username: {
            type: 'string',
            isRequired: true,
            maxLength: 255,
        },
        email: {
            type: 'any-of',
            contains: [{
                type: 'string',
                format: 'email',
                maxLength: 255,
            }, {
                type: 'null',
            }],
        },
        hashedPassword: {
            type: 'string',
            isRequired: true,
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
                maxLength: 40,
                minLength: 8,
            }, {
                type: 'null',
            }],
        },
    },
} as const;
