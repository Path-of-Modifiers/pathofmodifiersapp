/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $PlotQuery = {
    description: `Plots for items with or without modifiers`,
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
        end: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
        start: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
        wantedModifiers: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'array',
                    contains: {
                        type: 'WantedModifier',
                    },
                },
            }, {
                type: 'null',
            }],
        },
    },
} as const;
