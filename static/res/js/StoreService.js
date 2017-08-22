
var StoreService = function (type) {
    this.name = '/StoreService.svc';
    this.type = type ? type : 'GET';
    this.ListMove = function (p, onResult, onError) { return this.implement('ListMove', p, onResult, onError); };
    this.ListMove.params = { type: '' };
    this.SetMove = function (p, onResult, onError) { return this.implement('SetMove', p, onResult, onError); };
    this.SetMove.params = { obj: '' };
    this.RemoveMove = function (p, onResult, onError) { return this.implement('RemoveMove', p, onResult, onError); };
    this.RemoveMove.params = { id: '' };
    this.SumStore = function (p, onResult, onError) { return this.implement('SumStore', p, onResult, onError); };
    this.SumStore.params = { date: '' };

};
StoreService.prototype =
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
        // url = url.replace(':1033', ':8090');
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