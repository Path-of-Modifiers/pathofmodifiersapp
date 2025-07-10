/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Datum } from './Datum';
export type TimeseriesData = {
    name: string;
    data: Array<Datum>;
    confidenceRating: 'low' | 'medium' | 'high';
};

