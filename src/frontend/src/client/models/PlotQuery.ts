/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseSpecs } from './BaseSpecs';
import type { ItemSpecs } from './ItemSpecs';
import type { WantedModifier } from './WantedModifier';
export type PlotQuery = {
    league: string;
    itemSpecifications: ItemSpecs;
    baseSpecifications?: (BaseSpecs | null);
    wantedModifiers: Array<WantedModifier>;
};

