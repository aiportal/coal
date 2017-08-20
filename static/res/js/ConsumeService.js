
var ConsumeService = function (type) {
    this.name = '/ConsumeService.svc';
    this.type = type ? type : 'GET';
    this.ListFireIn = function (p, onResult, onError) { return this.implement('ListFireIn', p, onResult, onError); };
    this.ListFireIn.params = {};
    this.SetFireIn = function (p, onResult, onError) { return this.implement('SetFireIn', p, onResult, onError); };
    this.SetFireIn.params = { obj: '' };
    this.RemoveFireIn = function (p, onResult, onError) { return this.implement('RemoveFireIn', p, onResult, onError); };
    this.RemoveFireIn.params = { id: '' };
    this.ListSendOut = function (p, onResult, onError) { return this.implement('ListSendOut', p, onResult, onError); };
    this.ListSendOut.params = {};
    this.SetSendOut = function (p, onResult, onError) { return this.implement('SetSendOut', p, onResult, onError); };
    this.SetSendOut.params = { obj: '' };
    this.RemoveSendOut = function (p, onResult, onError) { return this.implement('RemoveSendOut', p, onResult, onError); };
    this.RemoveSendOut.params = { id: '' };
    this.ListRecord = function (p, onResult, onError) { return this.implement('ListRecord', p, onResult, onError); };
    this.ListRecord.params = {};
    this.SetRecord = function (p, onResult, onError) { return this.implement('SetRecord', p, onResult, onError); };
    this.SetRecord.params = { obj: '' };
    this.RemoveRecord = function (p, onResult, onError) { return this.implement('RemoveRecord', p, onResult, onError); };
    this.RemoveRecord.params = { id: '' };
    this.SumConsume = function (p, onResult, onError) { return this.implement('SumConsume', p, onResult, onError); };
    this.SumConsume.params = { start: '', end: '' };

};
ConsumeService.prototype =
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
        url = url.replace(':1033', ':8090');
        // for (var attr in prams)
        //     prams[attr] = prams[attr] ? escape(prams[attr]) : prams[attr];
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