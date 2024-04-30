"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.request = exports.catchErrorCodes = exports.getResponseBody = exports.getResponseHeader = exports.sendRequest = exports.getRequestBody = exports.getHeaders = exports.resolve = exports.getFormData = exports.getQueryString = exports.base64 = exports.isSuccess = exports.isFormData = exports.isBlob = exports.isStringWithValue = exports.isString = exports.isDefined = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
var axios_1 = require("axios");
var form_data_1 = require("form-data");
var ApiError_1 = require("./ApiError");
var CancelablePromise_1 = require("./CancelablePromise");
var isDefined = function (value) {
    return value !== undefined && value !== null;
};
exports.isDefined = isDefined;
var isString = function (value) {
    return typeof value === 'string';
};
exports.isString = isString;
var isStringWithValue = function (value) {
    return (0, exports.isString)(value) && value !== '';
};
exports.isStringWithValue = isStringWithValue;
var isBlob = function (value) {
    return (typeof value === 'object' &&
        typeof value.type === 'string' &&
        typeof value.stream === 'function' &&
        typeof value.arrayBuffer === 'function' &&
        typeof value.constructor === 'function' &&
        typeof value.constructor.name === 'string' &&
        /^(Blob|File)$/.test(value.constructor.name) &&
        /^(Blob|File)$/.test(value[Symbol.toStringTag]));
};
exports.isBlob = isBlob;
var isFormData = function (value) {
    return value instanceof form_data_1.default;
};
exports.isFormData = isFormData;
var isSuccess = function (status) {
    return status >= 200 && status < 300;
};
exports.isSuccess = isSuccess;
var base64 = function (str) {
    try {
        return btoa(str);
    }
    catch (err) {
        // @ts-ignore
        return Buffer.from(str).toString('base64');
    }
};
exports.base64 = base64;
var getQueryString = function (params) {
    var qs = [];
    var append = function (key, value) {
        qs.push("".concat(encodeURIComponent(key), "=").concat(encodeURIComponent(String(value))));
    };
    var process = function (key, value) {
        if ((0, exports.isDefined)(value)) {
            if (Array.isArray(value)) {
                value.forEach(function (v) {
                    process(key, v);
                });
            }
            else if (typeof value === 'object') {
                Object.entries(value).forEach(function (_a) {
                    var k = _a[0], v = _a[1];
                    process("".concat(key, "[").concat(k, "]"), v);
                });
            }
            else {
                append(key, value);
            }
        }
    };
    Object.entries(params).forEach(function (_a) {
        var key = _a[0], value = _a[1];
        process(key, value);
    });
    if (qs.length > 0) {
        return "?".concat(qs.join('&'));
    }
    return '';
};
exports.getQueryString = getQueryString;
var getUrl = function (config, options) {
    var encoder = config.ENCODE_PATH || encodeURI;
    var path = options.url
        .replace('{api-version}', config.VERSION)
        .replace(/{(.*?)}/g, function (substring, group) {
        var _a;
        if ((_a = options.path) === null || _a === void 0 ? void 0 : _a.hasOwnProperty(group)) {
            return encoder(String(options.path[group]));
        }
        return substring;
    });
    var url = "".concat(config.BASE).concat(path);
    if (options.query) {
        return "".concat(url).concat((0, exports.getQueryString)(options.query));
    }
    return url;
};
var getFormData = function (options) {
    if (options.formData) {
        var formData_1 = new form_data_1.default();
        var process_1 = function (key, value) {
            if ((0, exports.isString)(value) || (0, exports.isBlob)(value)) {
                formData_1.append(key, value);
            }
            else {
                formData_1.append(key, JSON.stringify(value));
            }
        };
        Object.entries(options.formData)
            .filter(function (_a) {
            var _ = _a[0], value = _a[1];
            return (0, exports.isDefined)(value);
        })
            .forEach(function (_a) {
            var key = _a[0], value = _a[1];
            if (Array.isArray(value)) {
                value.forEach(function (v) { return process_1(key, v); });
            }
            else {
                process_1(key, value);
            }
        });
        return formData_1;
    }
    return undefined;
};
exports.getFormData = getFormData;
var resolve = function (options, resolver) { return __awaiter(void 0, void 0, void 0, function () {
    return __generator(this, function (_a) {
        if (typeof resolver === 'function') {
            return [2 /*return*/, resolver(options)];
        }
        return [2 /*return*/, resolver];
    });
}); };
exports.resolve = resolve;
var getHeaders = function (config, options, formData) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, token, username, password, additionalHeaders, formHeaders, headers, credentials;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0: return [4 /*yield*/, Promise.all([
                    (0, exports.resolve)(options, config.TOKEN),
                    (0, exports.resolve)(options, config.USERNAME),
                    (0, exports.resolve)(options, config.PASSWORD),
                    (0, exports.resolve)(options, config.HEADERS),
                ])];
            case 1:
                _a = _b.sent(), token = _a[0], username = _a[1], password = _a[2], additionalHeaders = _a[3];
                formHeaders = typeof (formData === null || formData === void 0 ? void 0 : formData.getHeaders) === 'function' && (formData === null || formData === void 0 ? void 0 : formData.getHeaders()) || {};
                headers = Object.entries(__assign(__assign(__assign({ Accept: 'application/json' }, additionalHeaders), options.headers), formHeaders))
                    .filter(function (_a) {
                    var _ = _a[0], value = _a[1];
                    return (0, exports.isDefined)(value);
                })
                    .reduce(function (headers, _a) {
                    var _b;
                    var key = _a[0], value = _a[1];
                    return (__assign(__assign({}, headers), (_b = {}, _b[key] = String(value), _b)));
                }, {});
                if ((0, exports.isStringWithValue)(token)) {
                    headers['Authorization'] = "Bearer ".concat(token);
                }
                if ((0, exports.isStringWithValue)(username) && (0, exports.isStringWithValue)(password)) {
                    credentials = (0, exports.base64)("".concat(username, ":").concat(password));
                    headers['Authorization'] = "Basic ".concat(credentials);
                }
                if (options.body !== undefined) {
                    if (options.mediaType) {
                        headers['Content-Type'] = options.mediaType;
                    }
                    else if ((0, exports.isBlob)(options.body)) {
                        headers['Content-Type'] = options.body.type || 'application/octet-stream';
                    }
                    else if ((0, exports.isString)(options.body)) {
                        headers['Content-Type'] = 'text/plain';
                    }
                    else if (!(0, exports.isFormData)(options.body)) {
                        headers['Content-Type'] = 'application/json';
                    }
                }
                return [2 /*return*/, headers];
        }
    });
}); };
exports.getHeaders = getHeaders;
var getRequestBody = function (options) {
    if (options.body) {
        return options.body;
    }
    return undefined;
};
exports.getRequestBody = getRequestBody;
var sendRequest = function (config, options, url, body, formData, headers, onCancel, axiosClient) { return __awaiter(void 0, void 0, void 0, function () {
    var source, requestConfig, error_1, axiosError;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                source = axios_1.default.CancelToken.source();
                requestConfig = {
                    url: url,
                    headers: headers,
                    data: body !== null && body !== void 0 ? body : formData,
                    method: options.method,
                    withCredentials: config.WITH_CREDENTIALS,
                    withXSRFToken: config.CREDENTIALS === 'include' ? config.WITH_CREDENTIALS : false,
                    cancelToken: source.token,
                };
                onCancel(function () { return source.cancel('The user aborted a request.'); });
                _a.label = 1;
            case 1:
                _a.trys.push([1, 3, , 4]);
                return [4 /*yield*/, axiosClient.request(requestConfig)];
            case 2: return [2 /*return*/, _a.sent()];
            case 3:
                error_1 = _a.sent();
                axiosError = error_1;
                if (axiosError.response) {
                    return [2 /*return*/, axiosError.response];
                }
                throw error_1;
            case 4: return [2 /*return*/];
        }
    });
}); };
exports.sendRequest = sendRequest;
var getResponseHeader = function (response, responseHeader) {
    if (responseHeader) {
        var content = response.headers[responseHeader];
        if ((0, exports.isString)(content)) {
            return content;
        }
    }
    return undefined;
};
exports.getResponseHeader = getResponseHeader;
var getResponseBody = function (response) {
    if (response.status !== 204) {
        return response.data;
    }
    return undefined;
};
exports.getResponseBody = getResponseBody;
var catchErrorCodes = function (options, result) {
    var _a, _b;
    var errors = __assign({ 400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found', 500: 'Internal Server Error', 502: 'Bad Gateway', 503: 'Service Unavailable' }, options.errors);
    var error = errors[result.status];
    if (error) {
        throw new ApiError_1.ApiError(options, result, error);
    }
    if (!result.ok) {
        var errorStatus = (_a = result.status) !== null && _a !== void 0 ? _a : 'unknown';
        var errorStatusText = (_b = result.statusText) !== null && _b !== void 0 ? _b : 'unknown';
        var errorBody = (function () {
            try {
                return JSON.stringify(result.body, null, 2);
            }
            catch (e) {
                return undefined;
            }
        })();
        throw new ApiError_1.ApiError(options, result, "Generic Error: status: ".concat(errorStatus, "; status text: ").concat(errorStatusText, "; body: ").concat(errorBody));
    }
};
exports.catchErrorCodes = catchErrorCodes;
/**
 * Request method
 * @param config The OpenAPI configuration object
 * @param options The request options from the service
 * @param axiosClient The axios client instance to use
 * @returns CancelablePromise<T>
 * @throws ApiError
 */
var request = function (config, options, axiosClient) {
    if (axiosClient === void 0) { axiosClient = axios_1.default; }
    return new CancelablePromise_1.CancelablePromise(function (resolve, reject, onCancel) { return __awaiter(void 0, void 0, void 0, function () {
        var url, formData, body, headers, response, responseBody, responseHeader, result, error_2;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 4, , 5]);
                    url = getUrl(config, options);
                    formData = (0, exports.getFormData)(options);
                    body = (0, exports.getRequestBody)(options);
                    return [4 /*yield*/, (0, exports.getHeaders)(config, options, formData)];
                case 1:
                    headers = _a.sent();
                    if (!!onCancel.isCancelled) return [3 /*break*/, 3];
                    return [4 /*yield*/, (0, exports.sendRequest)(config, options, url, body, formData, headers, onCancel, axiosClient)];
                case 2:
                    response = _a.sent();
                    responseBody = (0, exports.getResponseBody)(response);
                    responseHeader = (0, exports.getResponseHeader)(response, options.responseHeader);
                    result = {
                        url: url,
                        ok: (0, exports.isSuccess)(response.status),
                        status: response.status,
                        statusText: response.statusText,
                        body: responseHeader !== null && responseHeader !== void 0 ? responseHeader : responseBody,
                    };
                    (0, exports.catchErrorCodes)(options, result);
                    resolve(result.body);
                    _a.label = 3;
                case 3: return [3 /*break*/, 5];
                case 4:
                    error_2 = _a.sent();
                    reject(error_2);
                    return [3 /*break*/, 5];
                case 5: return [2 /*return*/];
            }
        });
    }); });
};
exports.request = request;
