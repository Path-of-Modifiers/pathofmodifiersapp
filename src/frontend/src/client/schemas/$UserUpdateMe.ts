/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserUpdateMe = {
    properties: {
        email: {
            type: 'any-of',
            contains: [{
                type: 'string',
                format: 'email',
            }, {
                type: 'null',
            }],
        },
        username: {
            type: 'any-of',
            contains: [{
                type: 'string',
                pattern: '^[\\p{L}\\p{N}_]+$',
            }, {
                type: 'null',
            }],
        },
    },
} as const;
