
var Configuration = function (type) {
    this.name = '/Configuration.svc';
    this.type = type ? type : 'GET';
    this.ListBalance = function (p, onResult, onError) { return this.implement('ListBalance', p, onResult, onError); };
    this.ListBalance.params = {};
    this.SetBalance = function (p, onResult, onError) { return this.implement('SetBalance', p, onResult, onError); };
    this.SetBalance.params = { obj: '' };
    this.RemoveBalance = function (p, onResult, onError) { return this.implement('RemoveBalance', p, onResult, onError); };
    this.RemoveBalance.params = { id: '' };
    this.ListStorage = function (p, onResult, onError) { return this.implement('ListStorage', p, onResult, onError); };
    this.ListStorage.params = {};
    this.SetStorage = function (p, onResult, onError) { return this.implement('SetStorage', p, onResult, onError); };
    this.SetStorage.params = { obj: '' };
    this.RemoveStorage = function (p, onResult, onError) { return this.implement('RemoveStorage', p, onResult, onError); };
    this.RemoveStorage.params = { id: '' };
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