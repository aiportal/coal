
var CheckService = function (type) {
    this.name = '/CheckService.svc';
    this.type = type ? type : 'GET';
    this.ListCheckIn = function (p, onResult, onError) { return this.implement('ListCheckIn', p, onResult, onError); };
    this.ListCheckIn.params = {};
    this.SetCheckIn = function (p, onResult, onError) { return this.implement('SetCheckIn', p, onResult, onError); };
    this.SetCheckIn.params = { obj: '' };
    this.RemoveCheckIn = function (p, onResult, onError) { return this.implement('RemoveCheckIn', p, onResult, onError); };
    this.RemoveCheckIn.params = { id: '' };
    this.ListCheckOut = function (p, onResult, onError) { return this.implement('ListCheckOut', p, onResult, onError); };
    this.ListCheckOut.params = {};
    this.SetCheckOut = function (p, onResult, onError) { return this.implement('SetCheckOut', p, onResult, onError); };
    this.SetCheckOut.params = { obj: '' };
    this.SumCheckIn = function (p, onResult, onError) { return this.implement('SumCheckIn', p, onResult, onError); };
    this.SumCheckIn.params = {};

};
CheckService.prototype =
{
    ajaxInvoke: function (url, prams, onResult, onError) {
        $.support.cors = true;
        $.ajax({
            url: url,
            type: this.type,
            data: prams,
            cache: false,
            dataType: 'json',
            success: function (data) {
                if (!data || !data.Exception)
                    onResult(data);
                else if (onError)
                    onError(data);
            },
            error: function (request) {
                if (onError)
                    onError(request.responseText);
            }
        });
    },
    implement: function (method, prams, onResult, onError) {
        var url = 'http://' + location.host + this.name + '?$m=' + method;
        // for (var attr in prams)
        //     prams[attr] = prams[attr] ? encodeURI(prams[attr]) : prams[attr];
        if (onResult) {
            this.ajaxInvoke(url, prams, onResult, onError);
        }
        else {
            for (var attr in prams)
                url += prams[attr] ? '&' + attr + '=' + prams[attr] : '';
            return url;
        }
    }
};