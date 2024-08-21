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
                maxLength: 255,
            }, {
                type: 'null',
            }],
        },
        username: {
            type: 'any-of',
            contains: [{
                type: 'string',
                maxLength: 255,
            }, {
                type: 'null',
            }],
        },
    },
} as const;
