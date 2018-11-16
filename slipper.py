#!/usr/bin/env python
# coding=utf-8

import json

import aiohttp

__all__ = ["Response", "Session", "requests"]

TEXT = "text"
JSON = "json"
READ = "read"
RELEASE = "release"
GET_ENCODING = "get_encoding"
CLOSE = "close"
RAISE_FOR_STATUS = "raise_for_status"

URL = "url"
STATUS = "status"
VERSION = "version"
REASON = "reason"
REAL_URL = "real_url"
CONNECTION = "connection"
CONTENT = "content"
COOKIES = "cookies"
HEADERS = "headers"
RAW_HEADERS = "raw_headers"
LINKS = "links"
CONTENT_TYPE = "content_type"
CHARSET = "charset"
CONTENT_DISPOSITION = "content_disposition"
HISTORY = "history"
REQUEST_INFO = "request_info"

ALL_ATTRS = "all_attrs"


class AttrResponse:
    """
    Response Attribute class
    """

    url = [URL]
    status = [STATUS]
    version = [VERSION]
    reason = [REASON]
    real_url = [REAL_URL]
    connection = [CONNECTION]
    content = [CONTENT]
    cookies = [COOKIES]
    headers = [HEADERS]
    raw_headers = [RAW_HEADERS]
    links = [LINKS]
    content_type = [CONTENT_TYPE]
    charset = [CHARSET]
    content_disposition = [CONTENT_DISPOSITION]
    history = [HISTORY]
    all_attrs = [ALL_ATTRS]
    request_info = [REQUEST_INFO]


class FuncResponse:
    """
    Response Function class
    """

    @staticmethod
    def text(encoding=None):
        return TEXT, dict(encoding=encoding)

    @staticmethod
    def json(encoding=None, loads=json.loads, content_type="application/json"):
        return (JSON, dict(encoding=encoding, loads=loads, content_type=content_type))

    @staticmethod
    def read():
        return READ

    @staticmethod
    def release():
        return RELEASE

    @staticmethod
    def get_encoding():
        return GET_ENCODING

    @staticmethod
    def close():
        return CLOSE

    @staticmethod
    def raise_for_status():
        return RAISE_FOR_STATUS


class Response(FuncResponse, AttrResponse):
    """
    Response class, Inherited from Function class and Attribute class

    *Attrs*
    -------
    version:
        Response’s version, HttpVersion instance.
    status:
        HTTP status code of response (int), e.g. 200.
    reason:
        HTTP status reason of response (str), e.g. "OK".
    method:
        Request’s method (str).
    url:
        URL of request (URL).
    real_url:
        Unmodified URL of request (URL).
    connection:
        Connection used for handling response.
    content:
        Payload stream, which contains response’s BODY (StreamReader).
        It supports various reading methods depending on the expected
        format. When chunked transfer encoding is used by the server,
        allows retrieving the actual http chunks.

        Reading from the stream may raise aiohttp.ClientPayloadError
        if the response object is closed before response receives
        all data or in case if any transfer encoding related errors
        like misformed chunked encoding of broken compression data.
    cookies:
        HTTP cookies of response (Set-Cookie HTTP header, SimpleCookie).
    headers:
        A case-insensitive multidict proxy with HTTP headers
        of response, CIMultiDictProxy.
    raw_headers:
        Unmodified HTTP headers of response as unconverted bytes,
        a sequence of (key, value) pairs.
    links:
        Link HTTP header parsed into a MultiDictProxy.
        For each link, key is link param rel when it exists, or link
        url as str otherwise, and value is MultiDictProxy of link
        params and url at key url as URL instance.
    content_type:
        Read-only property with content part of Content-Type header.
    charset:
        Read-only property that specifies the encoding for the request’s BODY.
        The value is parsed from the Content-Type HTTP header.
        Returns str like 'utf-8' or None if no Content-Type header
        present in HTTP headers or it has no charset information.
    content_disposition:
        Read-only property that specified the Content-Disposition HTTP header.
        Instance of ContentDisposition or None if no Content-Disposition
        header present in HTTP headers.
    history:
        A Sequence of ClientResponse objects of preceding requests (earliest
        request first) if there were redirects, an empty sequence otherwise.
    request_info:
        A namedtuple with request URL and headers from ClientRequest
        object, aiohttp.RequestInfo instance.

    *Funcs*
    -------
    close():
        Close response and underlying connection.
        For keep-alive support see release().
    raise_for_status():
        Raise an aiohttp.ClientResponseError if the response
        status is 400 or higher.
        Do nothing for success responses (less than 400).
    get_encoding():
        Automatically detect content encoding using charset info in
        Content-Type HTTP header. If this info is not exists or
        there are no appropriate codecs for encoding then cchardet / chardet is used.
        Beware that it is not always safe to use the result of this
        function to decode a response. Some encodings detected by
        cchardet are not known by Python (e.g. VISCII).
    read() - coroutine:
        Read the whole response’s body as bytes.
        Close underlying connection if data reading gets an error,
        release connection otherwise.
        Raise an aiohttp.ClientResponseError if the data can’t be read.
        Return bytes:	read BODY.
    release() - coroutine:
        It is not required to call release on the response object.
        When the client fully receives the payload, the underlying
        connection automatically returns back to pool.
        If the payload is not fully read, the connection is closed
    text(encoding=None) - coroutine:
        Read response’s body and return decoded str using
        specified encoding parameter.
        If encoding is None content encoding is autocalculated using
        Content-Type HTTP header and chardet tool if the header is
        not provided by server.

        cchardet is used with fallback to chardet if cchardet is not available.
        Close underlying connection if data reading gets an error,
        release connection otherwise.

        Parameters:	encoding (str) – text encoding used for BODY decoding,
                    or None for encoding autodetection (default).
        Return str:	decoded BODY
        Raises:	LookupError – if the encoding detected by chardet or
                cchardet is unknown by Python (e.g. VISCII).
    json(*, encoding=None, loads=json.loads, content_type='application/json') - coroutine:
        Read response’s body as JSON, return dict using specified encoding
        and loader. If data is not still available a read call will be done,
        If encoding is None content encoding is autocalculated using cchardet
        or chardet as fallback if cchardet is not available.

        if response’s content-type does not match content_type parameter
        aiohttp.ContentTypeError get raised. To disable content
        type check pass None value.

        Parameters:
        * encoding (str) – text encoding used for BODY decoding, or
        None for encoding autodetection (default).
        By the standard JSON encoding should be UTF-8 but practice beats
        purity: some servers return non-UTF responses. Autodetection
        works pretty fine anyway.
        * loads (callable) – callable() used for loading JSON data,
        json.loads() by default.
        * content_type (str) – specify response’s content-type, if content type does
        not match raise aiohttp.ClientResponseError. To disable content-type check,
        pass None as value. (default: application/json).
        Returns:
        BODY as JSON data parsed by loads parameter or None if BODY is
        empty or contains white-spaces only.
    """

    pass


class Session:
    """
    Session class，transfer ClientSession class initialization parameter
    """

    def __init__(
        self,
        *,
        connector=None,
        loop=None,
        cookies=None,
        headers=None,
        skip_auto_headers=None,
        auth=None,
        json_serialize=json.dumps,
        version=aiohttp.HttpVersion11,
        cookie_jar=None,
        read_timeout=None,
        conn_timeout=None,
        timeout=aiohttp.ClientTimeout(),
        raise_for_status=False,
        connector_owner=True,
        auto_decompress=True,
    ):
        """

        :param connector:
            (aiohttp.connector.BaseConnector) – BaseConnector
            sub-class instance to support connection pooling.
        :param loop:
            event loop used for processing HTTP requests. If loop is
            None the constructor borrows it from connector if
            specified.asyncio.get_event_loop() is used for getting
             default event loop otherwise.
        :param cookies:
            Cookies to send with the request (optional)
        :param headers:
            HTTP Headers to send with every request (optional).
            May be either iterable of key-value pairs or Mapping
            (e.g. dict, CIMultiDict).
        :param skip_auto_headers:
            set of headers for which autogeneration should be skipped.
            aiohttp autogenerates headers like User-Agent or Content-Type
            if these headers are not explicitly passed.
            Using skip_auto_headers parameter allows to skip that
            generation. Note that Content-Length autogeneration
            can’t be skipped. Iterable of str or istr (optional)
        :param auth:
            (aiohttp.BasicAuth) – an object that represents HTTP
            Basic Authorization (optional)
        :param json_serialize:
            Json serializer callable.By default json.dumps() function.
        :param version:
            supported HTTP version, HTTP 1.1 by default.
        :param cookie_jar:
            Cookie Jar, AbstractCookieJar instance.By default every
            session instance has own private cookie jar for automatic
            cookies processing but user may redefine this behavior
            by providing own jar implementation.
            One example is not processing cookies at all when
            working in proxy mode.
            If no cookie processing is needed, a aiohttp.DummyCookieJar
            instance can be provided.
        :param timeout:
            Request operations timeout. timeout is cumulative for all
            request operations (request, redirects, responses,
            data consuming). By default, the read timeout is 5*60 seconds.
            Use None or 0 to disable timeout checks.
        :param raise_for_status:
            ClientResponse.raise_for_status() for each response, False by default.
        :param connector_owner:
            Close connector instance on session closing.
            Setting the parameter to False allows to share connection pool
            between sessions without sharing session state: cookies etc.
        :param auto_decompress:
            Automatically decompress response body
        """
        self.params = dict(
            connector=connector,
            loop=loop,
            cookies=cookies,
            headers=headers,
            skip_auto_headers=skip_auto_headers,
            auth=auth,
            json_serialize=json_serialize,
            version=version,
            cookie_jar=cookie_jar,
            read_timeout=read_timeout,
            conn_timeout=conn_timeout,
            timeout=timeout,
            raise_for_status=raise_for_status,
            connector_owner=connector_owner,
            auto_decompress=auto_decompress,
        )


class Request:
    __instance = None
    __session_cfg = None

    @classmethod
    async def _get_session(cls, **kwargs):
        if not cls.__instance:
            cls.__instance = aiohttp.ClientSession(**kwargs)
        return cls.__instance

    @classmethod
    def global_session(cls, session):
        if not cls.__session_cfg:
            cls.__session_cfg = session

    @classmethod
    async def request(
        cls,
        method,
        url,
        *,
        params=None,
        client_sess=None,
        expect_resp=None,
        data=None,
        json=None,
        headers=None,
        skip_auto_headers=None,
        auth=None,
        allow_redirects=True,
        max_redirects=10,
        compress=None,
        chunked=None,
        expect100=False,
        read_until_eof=True,
        proxy=None,
        proxy_auth=None,
        timeout=aiohttp.ClientTimeout(),
        ssl=None,
        verify_ssl=None,
        fingerprint=None,
        ssl_context=None,
        proxy_headers=None,
    ):
        """

        :param method:
            HTTP method
        :param url:
             Request URL, str or URL.
        :param params:
            Mapping, iterable of tuple of key/value pairs or string to
            be sent as parameters in the query string of the new request.
            Ignored for subsequent redirected requests (optional)

            Allowed values are:
            * collections.abc.Mapping e.g. dict, aiohttp.MultiDict or
              aiohttp.MultiDictProxy
            * collections.abc.Iterable e.g. tuple or list
            * str with preferably url-encoded content (Warning: content
              will not be encoded by aiohttp)
        :param expect_resp:
            except Response type, could be any attrs/funcs in Response class
            example:
                expect_resp=Response.url
                except_resp=Response.text()
        :param client_sess:
            ClientSession() instantiation parameters dictionary
        :param data:
            Dictionary, bytes, or file-like object to send in the
            body of the request (optional)
        :param json:
            Any json compatible python object (optional). json and data
            parameters could not be used at the same time.
        :param headers:
            (dict) HTTP Headers to send with the request (optional)
        :param skip_auto_headers:
            set of headers for which autogeneration should be skipped.
            aiohttp autogenerates headers like User-Agent or Content-Type
            if these headers are not explicitly passed. Using skip_auto_headers
            parameter allows to skip that generation.
            Iterable of str or istr (optional)
        :param auth:
             an object that represents HTTP Basic Authorization (optional)
        :param allow_redirects:
            If set to False, do not follow redirects. True by default (optional).
        :param max_redirects:
            (int) - Maximum number of redirects to follow. 10 by default.
        :param compress:
            (bool) - Set to True if request has to be compressed with
            deflate encoding. If compress can not be combined with a
            Content-Encoding and Content-Length headers. None by default (optional).
        :param chunked:
            (int) – Enable chunked transfer encoding. It is up to the developer
            to decide how to chunk data streams. If chunking is enabled,
            aiohttp encodes the provided chunks in the “Transfer-encoding:
            chunked” format. If chunked is set, then the Transfer-encoding
            and content-length headers are disallowed. None by default (optional).
        :param expect100:
            (bool) – Expect 100-continue response from server.
            False by default (optional).
        :param read_until_eof:
            (bool) – Read response until EOF if response does not have
            Content-Length header. True by default (optional).
        :param proxy:
            proxy – Proxy URL, str or URL (optional)
        :param proxy_auth:
            (aiohttp.BasicAuth) - an object that represents proxy
            HTTP Basic Authorization (optional)
        :param timeout:
            override the session’s timeout.
            Changed in version 3.3: The parameter is ClientTimeout instance,
            float is still supported for sake of backward compatibility.
            If float is passed it is a total timeout.
        :param ssl:
            SSL validation mode. None for default SSL check
            (ssl.create_default_context() is used), False for skip
            SSL certificate validation, aiohttp.Fingerprint for fingerprint
            validation, ssl.SSLContext for custom SSL certificate validation.
            Supersedes verify_ssl, ssl_context and fingerprint parameters.
        :param verify_ssl:
            (bool) – Perform SSL certificate validation for HTTPS requests
            (enabled by default). May be disabled to skip validation
            for sites with invalid certificates.
        :param fingerprint:
            Pass the SHA256 digest of the expected certificate in DER format
            to verify that the certificate the server presents matches.
            Useful for certificate pinning.
            Warning: use of MD5 or SHA1 digests is insecure and removed.
        :param ssl_context:
            (ssl.SSLContext) – ssl context used for processing
            HTTPS requests (optional).
            ssl_context may be used for configuring certification authority
            channel, supported SSL options etc.
        :param proxy_headers:
            HTTP headers to send to the proxy if the parameter
            proxy has been provided.
        """
        gs = cls.__session_cfg
        if client_sess is None:
            kws = getattr(gs, "params", {})
            _client_session = await cls._get_session(**kws)
        else:
            _client_session = await cls._get_session(use_kw=True, **client_sess.params)
        async with _client_session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            skip_auto_headers=skip_auto_headers,
            auth=auth,
            allow_redirects=allow_redirects,
            max_redirects=max_redirects,
            compress=compress,
            chunked=chunked,
            expect100=expect100,
            read_until_eof=read_until_eof,
            proxy=proxy,
            proxy_auth=proxy_auth,
            timeout=timeout,
            ssl=ssl,
            verify_ssl=verify_ssl,
            fingerprint=fingerprint,
            ssl_context=ssl_context,
            proxy_headers=proxy_headers,
        ) as resp:

            func = keywords = None
            if expect_resp is None:
                func = STATUS
            else:
                if isinstance(expect_resp, (tuple, list)):
                    if len(expect_resp) > 1:
                        func, keywords = expect_resp
                    else:
                        func, = expect_resp
                elif isinstance(expect_resp, str):
                    func = expect_resp

            if func == TEXT:
                return await resp.text(**keywords)
            elif func == JSON:
                return await resp.json(**keywords)
            elif func == READ:
                return await resp.read()
            elif func == RELEASE:
                return await resp.release()
            elif func == GET_ENCODING:
                return resp.get_encoding()
            elif func == CLOSE:
                return resp.close()
            elif func == RAISE_FOR_STATUS:
                return resp.raise_for_status()

            all_attrs = dict(
                url=resp.url,
                version=resp.version,
                status=resp.status,
                reason=resp.reason,
                real_url=resp.real_url,
                connection=resp.connection,
                content=resp.content,
                cookies=resp.cookies,
                headers=resp.headers,
                raw_headers=resp.raw_headers,
                links=resp.links,
                content_type=resp.content_type,
                charset=resp.charset,
                content_disposition=resp.content_disposition,
                history=resp.history,
                request_info=resp.request_info,
            )

            if func == ALL_ATTRS:
                return all_attrs
            return all_attrs.get(func, None)

    def __del__(self):
        """
        Make sure session could be cloesd
        """
        _ins = self.__instance
        if _ins and not _ins.closed:
            if _ins._connector_owner:
                _ins._connector.close()
            _ins._connector = None

    @classmethod
    async def get(cls, url, *, expect_resp=None, client_sess=None, **kwargs):
        """

        :param url: Request URL, str or URL.
        :param expect_resp:
            except Response type, could be any attrs/funcs in Response class
            example:
                expect_resp=Response.url
                except_resp=Response.text()
        :param client_sess:
            ClientSession() instantiation parameters dictionary
        :param kwargs:
        """
        return await cls.request(
            "get", url, expect_resp=expect_resp, client_sess=client_sess, **kwargs
        )

    @classmethod
    async def options(cls, url, expect_resp=None, client_sess=None, **kwargs):
        """

        :param url: Request URL, str or URL.
        :param expect_resp: refer get()
        :param client_sess: refer get()
        :param kwargs:
        """
        return await cls.request(
            "options", url, expect_resp=expect_resp, client_sess=client_sess, **kwargs
        )

    @classmethod
    async def head(
        cls, url, allow_redirects=False, expect_resp=None, client_sess=None, **kwargs
    ):
        """

        :param url: Request URL, str or URL.
        :param allow_redirects: If set to False, do not follow redirects.
                                True by default (optional).
        :param expect_resp: refer get()
        :param client_sess: refer get()
        :param kwargs:
        """
        return await cls.request(
            "head",
            url,
            allow_redirects=allow_redirects,
            expect_resp=expect_resp,
            client_sess=client_sess,
            **kwargs,
        )

    @classmethod
    async def post(
        cls, url, data=None, json=None, expect_resp=None, client_sess=None, **kwargs
    ):
        """

        :param url: Request URL, str or URL.
        :param data: Dictionary, bytes, or file-like object to send in
                     the body of the request (optional)
        :param json: Any json compatible python object (optional). json and data
                     parameters could not be used at the same time.
        :param expect_resp: refer get()
        :param client_sess: refer get()
        :param kwargs:
        """
        return await cls.request(
            "post",
            url,
            data=data,
            json=json,
            expect_resp=expect_resp,
            client_sess=client_sess,
            **kwargs,
        )

    @classmethod
    async def put(cls, url, data=None, expect_resp=None, client_sess=None, **kwargs):
        """

        :param url: Request URL, str or URL.
        :param data: Dictionary, bytes, or file-like object to send in
                     the body of the request (optional)
        :param expect_resp: refer get()
        :param client_sess: refer get()
        :param kwargs:
        """
        return await cls.request(
            "put",
            url,
            data=data,
            expect_resp=expect_resp,
            client_sess=client_sess,
            **kwargs,
        )

    @classmethod
    async def patch(cls, url, data=None, expect_resp=None, client_sess=None, **kwargs):
        """

        :param url: Request URL, str or URL.
        :param data: Dictionary, bytes, or file-like object to send in
                     the body of the request (optional)
        :param expect_resp: refer get()
        :param client_sess: refer get()
        :param kwargs:
        """
        return await cls.request(
            "patch",
            url,
            expect_resp=expect_resp,
            data=data,
            client_sess=client_sess,
            **kwargs,
        )

    @classmethod
    async def delete(cls, url, expect_resp=None, client_sess=None, **kwargs):
        """

        :param url: Request URL, str or URL.
        :param expect_resp: refer get()
        :param client_sess: refer get()
        :param kwargs:
        """
        return await cls.request(
            "delete", url, expect_resp=expect_resp, client_sess=client_sess, **kwargs
        )


requests = Request()
