/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GroupedModifierByEffect } from '../models/GroupedModifierByEffect';
import type { Modifier } from '../models/Modifier';
import type { ModifierCreate } from '../models/ModifierCreate';
import type { ModifierUpdate } from '../models/ModifierUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ModifiersService {
    /**
     * Get Modifier
     * Get modifier or list of modifiers by key and
     * value for "modifierId" and optional "position"
     *
     * Dominant key is "modifierId".
     *
     * Returns one or a list of modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getModifierApiApiV1ModifierModifierIdGet({
        modifierId,
        position,
    }: {
        modifierId: string,
        position?: (number | null),
    }): CancelablePromise<(Modifier | Array<Modifier>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/modifier/{modifierId}',
            path: {
                'modifierId': modifierId,
            },
            query: {
                'position': position,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Modifier
     * Update a modifier by key and value for "modifierId" and "position".
     *
     * Dominant key is "modifierId".
     *
     * Returns the updated modifier.
     * @returns Modifier Successful Response
     * @throws ApiError
     */
    public static updateModifierApiApiV1ModifierModifierIdPut({
        modifierId,
        position,
        requestBody,
    }: {
        modifierId: number,
        position: number,
        requestBody: ModifierUpdate,
    }): CancelablePromise<Modifier> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/modifier/{modifierId}',
            path: {
                'modifierId': modifierId,
            },
            query: {
                'position': position,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Modifier
     * Delete a modifier by key and value for "modifierId"
     * and optional "position".
     *
     * Dominant key is "modifierId".
     *
     * Returns a message that the modifier was deleted.
     * Always deletes one modifier.
     * @returns string Successful Response
     * @throws ApiError
     */
    public static deleteModifierApiApiV1ModifierModifierIdDelete({
        modifierId,
        position,
    }: {
        modifierId: number,
        position?: (number | null),
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/modifier/{modifierId}',
            path: {
                'modifierId': modifierId,
            },
            query: {
                'position': position,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get All Modifiers
     * Get all modifiers.
     *
     * Returns a list of all modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllModifiersApiApiV1ModifierGet(): CancelablePromise<(Modifier | Array<Modifier>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/modifier/',
        });
    }
    /**
     * Create Modifier
     * Create one or a list of new modifiers.
     *
     * Returns the created modifier or list of modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createModifierApiApiV1ModifierPost({
        requestBody,
    }: {
        requestBody: (ModifierCreate | Array<ModifierCreate>),
    }): CancelablePromise<(ModifierCreate | Array<ModifierCreate>)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/modifier/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Grouped Modifier By Effect
     * Get all grouped modifiers by effect.
     *
     * Returns a list of all grouped modifiers by effect.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getGroupedModifierByEffectApiApiV1ModifierGroupedModifiersByEffectGet(): CancelablePromise<(GroupedModifierByEffect | Array<GroupedModifierByEffect>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/modifier/grouped_modifiers_by_effect/',
        });
    }
}
