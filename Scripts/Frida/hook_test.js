Java.perform(() => {
    var SignatureClass = Java.use('com.askfm.network.utils.Signature');
    var HttpRequestClass = Java.use('com.askfm.network.request.base.RequestData');

    SignatureClass.generateHashWithKey.overload('java.lang.String', 'java.lang.String', 'java.lang.String', 'java.lang.String', 'java.util.Map')
        .implementation = function (key, method, host, path, params) {
        send('Inside of generateHashWithKey new implementation');


        send('Key: ' + key);
        send('Method: ' + method);
        send('Host: ' + host);
        send('Path: ' + path);
        send('Params: ');

        var keySet = params.keySet().toArray();
        for (var i = 0; i < keySet.length; i++) {
            var paramKey = keySet[i];
            var paramValue = params.get(paramKey).toString();
            send(paramKey + ': ' + paramValue);
        }

        var retGen = this.generateHashWithKey(key, method, host, path, params);

        send('generateHashWithKey return value: ' + retGen);
        return retGen;
    };

    SignatureClass.sha1.overload('java.lang.String', 'java.lang.String')
        .implementation = function (str, keyString) {
        send('Inside of sha1 new implementation');
        send('String: ' + str);
        send('KeyString: ' + keyString);

        var retSha1 = this.sha1(str, keyString);

        send('sha1 return value: ' + retSha1);
        return retSha1;
    };

    HttpRequestClass.getRequestHeaders.implementation = function () {
        send('Inside of getRequestHeaders new implementation');
        var retReqHeaders = this.getRequestHeaders();

        send('Request Headers: ' + retReqHeaders);
        var keySet = retReqHeaders.keySet().toArray();
        for (var i = 0; i < keySet.length; i++) {
            var headerKey = keySet[i];
            var headerValue = retReqHeaders.get(headerKey).toString();
            send(headerKey + ': ' + headerValue);
        }
        return retReqHeaders;
    }
  });