
/*-----------------------------------------------------------------------------
Admin proxy (need Configuration.js)
-----------------------------------------------------------------------------*/

var Admin = function () {
    this.name = '/Login.svc';
    this.Login = function (p, func) { return this.implement('Login', p, func); };
    this.Login.params = { user: '', pwd: '' };
    this.Logout = function (p, func) { return this.implement('Logout', p, func); };
    this.Logout.params = {};
};
Admin.prototype = Configuration.prototype;
