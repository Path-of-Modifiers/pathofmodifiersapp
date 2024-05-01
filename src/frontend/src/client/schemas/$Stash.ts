/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Stash = {
    properties: {
        accountName: {
            type: 'string',
            isRequired: true,
        },
        public: {
            type: 'boolean',
            isRequired: true,
        },
        league: {
            type: 'string',
            isRequired: true,
        },
        stashId: {
            type: 'string',
            isRequired: true,
        },
        createdAt: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        updatedAt: {
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
