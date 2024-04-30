"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __classPrivateFieldSet = (this && this.__classPrivateFieldSet) || function (receiver, state, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return (kind === "a" ? f.call(receiver, value) : f ? f.value = value : state.set(receiver, value)), value;
};
var __classPrivateFieldGet = (this && this.__classPrivateFieldGet) || function (receiver, state, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state.get(receiver);
};
var _CancelablePromise_isResolved, _CancelablePromise_isRejected, _CancelablePromise_isCancelled, _CancelablePromise_cancelHandlers, _CancelablePromise_promise, _CancelablePromise_resolve, _CancelablePromise_reject;
Object.defineProperty(exports, "__esModule", { value: true });
exports.CancelablePromise = exports.CancelError = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
var CancelError = /** @class */ (function (_super) {
    __extends(CancelError, _super);
    function CancelError(message) {
        var _this = _super.call(this, message) || this;
        _this.name = 'CancelError';
        return _this;
    }
    Object.defineProperty(CancelError.prototype, "isCancelled", {
        get: function () {
            return true;
        },
        enumerable: false,
        configurable: true
    });
    return CancelError;
}(Error));
exports.CancelError = CancelError;
var CancelablePromise = /** @class */ (function () {
    function CancelablePromise(executor) {
        var _this = this;
        _CancelablePromise_isResolved.set(this, void 0);
        _CancelablePromise_isRejected.set(this, void 0);
        _CancelablePromise_isCancelled.set(this, void 0);
        _CancelablePromise_cancelHandlers.set(this, void 0);
        _CancelablePromise_promise.set(this, void 0);
        _CancelablePromise_resolve.set(this, void 0);
        _CancelablePromise_reject.set(this, void 0);
        __classPrivateFieldSet(this, _CancelablePromise_isResolved, false, "f");
        __classPrivateFieldSet(this, _CancelablePromise_isRejected, false, "f");
        __classPrivateFieldSet(this, _CancelablePromise_isCancelled, false, "f");
        __classPrivateFieldSet(this, _CancelablePromise_cancelHandlers, [], "f");
        __classPrivateFieldSet(this, _CancelablePromise_promise, new Promise(function (resolve, reject) {
            __classPrivateFieldSet(_this, _CancelablePromise_resolve, resolve, "f");
            __classPrivateFieldSet(_this, _CancelablePromise_reject, reject, "f");
            var onResolve = function (value) {
                if (__classPrivateFieldGet(_this, _CancelablePromise_isResolved, "f") || __classPrivateFieldGet(_this, _CancelablePromise_isRejected, "f") || __classPrivateFieldGet(_this, _CancelablePromise_isCancelled, "f")) {
                    return;
                }
                __classPrivateFieldSet(_this, _CancelablePromise_isResolved, true, "f");
                if (__classPrivateFieldGet(_this, _CancelablePromise_resolve, "f"))
                    __classPrivateFieldGet(_this, _CancelablePromise_resolve, "f").call(_this, value);
            };
            var onReject = function (reason) {
                if (__classPrivateFieldGet(_this, _CancelablePromise_isResolved, "f") || __classPrivateFieldGet(_this, _CancelablePromise_isRejected, "f") || __classPrivateFieldGet(_this, _CancelablePromise_isCancelled, "f")) {
                    return;
                }
                __classPrivateFieldSet(_this, _CancelablePromise_isRejected, true, "f");
                if (__classPrivateFieldGet(_this, _CancelablePromise_reject, "f"))
                    __classPrivateFieldGet(_this, _CancelablePromise_reject, "f").call(_this, reason);
            };
            var onCancel = function (cancelHandler) {
                if (__classPrivateFieldGet(_this, _CancelablePromise_isResolved, "f") || __classPrivateFieldGet(_this, _CancelablePromise_isRejected, "f") || __classPrivateFieldGet(_this, _CancelablePromise_isCancelled, "f")) {
                    return;
                }
                __classPrivateFieldGet(_this, _CancelablePromise_cancelHandlers, "f").push(cancelHandler);
            };
            Object.defineProperty(onCancel, 'isResolved', {
                get: function () { return __classPrivateFieldGet(_this, _CancelablePromise_isResolved, "f"); },
            });
            Object.defineProperty(onCancel, 'isRejected', {
                get: function () { return __classPrivateFieldGet(_this, _CancelablePromise_isRejected, "f"); },
            });
            Object.defineProperty(onCancel, 'isCancelled', {
                get: function () { return __classPrivateFieldGet(_this, _CancelablePromise_isCancelled, "f"); },
            });
            return executor(onResolve, onReject, onCancel);
        }), "f");
    }
    Object.defineProperty(CancelablePromise.prototype, (_CancelablePromise_isResolved = new WeakMap(), _CancelablePromise_isRejected = new WeakMap(), _CancelablePromise_isCancelled = new WeakMap(), _CancelablePromise_cancelHandlers = new WeakMap(), _CancelablePromise_promise = new WeakMap(), _CancelablePromise_resolve = new WeakMap(), _CancelablePromise_reject = new WeakMap(), Symbol.toStringTag), {
        get: function () {
            return "Cancellable Promise";
        },
        enumerable: false,
        configurable: true
    });
    CancelablePromise.prototype.then = function (onFulfilled, onRejected) {
        return __classPrivateFieldGet(this, _CancelablePromise_promise, "f").then(onFulfilled, onRejected);
    };
    CancelablePromise.prototype.catch = function (onRejected) {
        return __classPrivateFieldGet(this, _CancelablePromise_promise, "f").catch(onRejected);
    };
    CancelablePromise.prototype.finally = function (onFinally) {
        return __classPrivateFieldGet(this, _CancelablePromise_promise, "f").finally(onFinally);
    };
    CancelablePromise.prototype.cancel = function () {
        if (__classPrivateFieldGet(this, _CancelablePromise_isResolved, "f") || __classPrivateFieldGet(this, _CancelablePromise_isRejected, "f") || __classPrivateFieldGet(this, _CancelablePromise_isCancelled, "f")) {
            return;
        }
        __classPrivateFieldSet(this, _CancelablePromise_isCancelled, true, "f");
        if (__classPrivateFieldGet(this, _CancelablePromise_cancelHandlers, "f").length) {
            try {
                for (var _i = 0, _a = __classPrivateFieldGet(this, _CancelablePromise_cancelHandlers, "f"); _i < _a.length; _i++) {
                    var cancelHandler = _a[_i];
                    cancelHandler();
                }
            }
            catch (error) {
                console.warn('Cancellation threw an error', error);
                return;
            }
        }
        __classPrivateFieldGet(this, _CancelablePromise_cancelHandlers, "f").length = 0;
        if (__classPrivateFieldGet(this, _CancelablePromise_reject, "f"))
            __classPrivateFieldGet(this, _CancelablePromise_reject, "f").call(this, new CancelError('Request aborted'));
    };
    Object.defineProperty(CancelablePromise.prototype, "isCancelled", {
        get: function () {
            return __classPrivateFieldGet(this, _CancelablePromise_isCancelled, "f");
        },
        enumerable: false,
        configurable: true
    });
    return CancelablePromise;
}());
exports.CancelablePromise = CancelablePromise;
