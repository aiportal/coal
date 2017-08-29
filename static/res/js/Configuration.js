
var Configuration = function (type) {
    this.name = '/Config.svc';
    this.type = type ? type : 'GET';
    this.ListItem = function (p, onResult, onError) { return this.implement('ListItem', p, onResult, onError); };
    this.ListItem.params = {};
    this.SetItem = function (p, onResult, onError) { return this.implement('SetItem', p, onResult, onError); };
    this.SetItem.params = { prams: '' };
    this.RemoveItem = function (p, onResult, onError) { return this.implement('RemoveItem', p, onResult, onError); };
    this.RemoveItem.params = { prams: '' };

    this.GetLicenseInfo = function (p, onResult, onError) { return this.implement('GetLicenseInfo', p, onResult, onError); };
    this.GetLicenseInfo.params = {};
    this.RegisterLicense = function (p, onResult, onError) { return this.implement('RegisterLicense', p, onResult, onError); };
    this.RegisterLicense.params = { lic: '' };
    this.GetConfigurations = function (p, onResult, onError) { return this.implement('GetConfigurations', p, onResult, onError); };
    this.GetConfigurations.params = {};
    this.SetConfigurations = function (p, onResult, onError) { return this.implement('SetConfigurations', p, onResult, onError); };
    this.SetConfigurations.params = { prams: '' };
    this.SetAdminPassword = function (p, onResult, onError) { return this.implement('SetAdminPassword', p, onResult, onError); };
    this.SetAdminPassword.params = { pwd: '' };

};
Configuration.prototype =
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
        for (var attr in prams)
            prams[attr] = prams[attr] ? escape(prams[attr]) : prams[attr];
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