/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseSpecs } from './BaseSpecs';
import type { ItemSpecs } from './ItemSpecs';
import type { WantedModifier } from './WantedModifier';
/**
 * Plots for items with or without modifiers
 */
export type PlotQuery = {
    league: (Array<string> | string);
    itemSpecifications?: (ItemSpecs | null);
    baseSpecifications?: (BaseSpecs | null);
    end?: (number | null);
    start?: (number | null);
    wantedModifiers?: (Array<Array<WantedModifier>> | null);
    dataPointsPerHour?: number;
};

