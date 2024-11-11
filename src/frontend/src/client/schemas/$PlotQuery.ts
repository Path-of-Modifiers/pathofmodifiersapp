/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $PlotQuery = {
    properties: {
        league: {
            type: 'string',
            isRequired: true,
        },
        itemSpecifications: {
            type: 'any-of',
            contains: [{
                type: 'ItemSpecs',
            }, {
                type: 'null',
            }],
        },
        baseSpecifications: {
            type: 'any-of',
            contains: [{
                type: 'BaseSpecs',
            }, {
                type: 'null',
            }],
        },
        wantedModifiers: {
            type: 'array',
            contains: {
                type: 'array',
                contains: {
                    type: 'WantedModifier',
                },
            },
            isRequired: true,
        },
    },
} as const;
