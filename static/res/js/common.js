/*-----------------------------------------------------------------------------
    common functions
-----------------------------------------------------------------------------*/

$(function () {
    $('[href=#]').attr('href', 'javascript:void(0);');
});

if ($.fn.datebox) {
    $.fn.datebox.defaults.formatter = function (date) {
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        var d = date.getDate();
        return y + '-' + (m < 10 ? ('0' + m) : m) + '-' + (d < 10 ? ('0' + d) : d);
    };
    $.fn.datebox.defaults.value = $.fn.datebox.defaults.formatter(new Date());
}

if ($.fn.timespinner) {
    $.fn.timespinner.defaults.formatter = function (date) {
        var h = date.getHours();
        var m = date.getMinutes();
        return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m;
    }
}

function date_value(days) {
    var date = new Date();
    if (days)
        date.setDate(date.getDate() + days);
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    var d = date.getDate();
    return y + '-' + (m < 10 ? ('0' + m) : m) + '-' + (d < 10 ? ('0' + d) : d);
}

function bold_format(val, txt) {
    if (val && val.length > 0 && txt && txt.length > 0) {
        var v = escape(val);
        var t = escape(txt).replace(/\//g, '\\/').replace(/\*/g, '\\*');
        try {
            val = unescape(eval("v.replace(/" + t + "/ig, '<b>$&</b>')"));
        }
        catch (err) { }
        val = val.replace(/\r\n/g, '<br/>');
    }
    return val;
}

function str_compare(a, b) {
    a = (a + '').toLowerCase();
    b = (b + '').toLowerCase();
    return a.localeCompare(b);
}

function fmt_password(val) {
    return '********';
}

function fmt_ton(v) {
    return ($.isNumeric(v) ? parseFloat(v).toFixed(3) : v) + ' 吨';
}

function err_apply(err) {
    if (err && err.Exception) {
        $.messager.alert('错误', err.Exception);
    }
    else {
        $.messager.show({ title: '错误', msg: '操作未成功!', showType: 'show' });
    }
}

/*-----------------------------------------------------------------------------
custom grid
-----------------------------------------------------------------------------*/
if ($.fn.formgrid) {
    $.extend($.fn.formgrid.defaults, {
        noheader: true,
        fit: true,
        rownumbers: true,
        striped: true,
        showFooter: true,
        singleSelect: true,
        remoteSort: false,
        bodyCls: 'grid_body',
        toolbar: '#toolbar',
        idField: 'ID',
        tipMsg: {
            norecord: {
                title: '提示',
                msg: '未选中任何记录.'
            },
            confirm: {
                title: '确认',
                msg: '确认要删除这条记录?'
            }
        },
        onError: function (idx, data) {
            if (data && data.Exception) {
                $.messager.alert('错误', data.Exception);
            }
            else {
                $.messager.show({ title: '错误', msg: '操作未成功!', showType: 'show' });
            }
        }
    });
}

/*-----------------------------------------------------------------------------
common editors
-----------------------------------------------------------------------------*/
$.extend($.fn.datagrid.defaults.editors, {
    password: {
        init: function (container, options) {
            var input = $('<input type="password" />').appendTo(container);
            setTimeout(function () {
                $(input).validatebox($.extend({}, options));
            });
            return input;
        },
        destroy: function (target) {
            $(target).remove();
        },
        getValue: function (target) {
            return $(target).val();
        },
        setValue: function (target, value) {
            $(target).val(value);
        },
        resize: function (target, width) {
            $(target)._outerWidth(width);
        }
    },
    dropdown: {
        init: function (container, options) {
            var input = $('<input type="text" />').appendTo(container);
            var vals = options.items.split(',');
            setTimeout(function () {
                $(input).combobox($.extend({}, options, {
                    editable: false,
                    panelHeight: 'auto',
                    loader: function (param, success, error) {
                        var rows = [];
                        $(vals).each(function (k, v) {
                            rows.push({ value: v, text: v });
                        });
                        success(rows);
                    }
                }));
            }, 0);
            return input;
        },
        destroy: function (target) {
            $(target).remove();
        },
        getValue: function (target) {
            return $(target).combobox('getText');
        },
        setValue: function (target, value) {
            $(target).val(value);
        },
        resize: function (target, width) {
            $(target)._outerWidth(width);
        }
    }
});

$.extend($.fn.datagrid.defaults.editors, {
    boolean: {
        init: function (container, options) {
            var input = $('<input type="checkbox" />').appendTo(container);
            setTimeout(function () {
            });
            return input;
        },
        destroy: function (target) {
            $(target).remove();
        },
        getValue: function (target) {
            return $(target).is(':checked');
        },
        setValue: function (target, value) {
            $(target).prop('checked',value);
        },
        resize: function (target, width) {
            $(target)._outerWidth(width);
        }
    },
    datetime: {
        init: function (container, options) {
            var input = $('<input />').appendTo(container);
            setTimeout(function () {
                $(input).datetimebox($.extend({
                    showSeconds: false
                }, options));
            });
            return input;
        },
        destroy: function (target) {
            $(target).remove();
        },
        getValue: function (target) {
            return $(target).datetimebox('getValue')
        },
        setValue: function (target, value) {
            $(target).val(value);
        },
        resize: function (target, width) {
            $(target)._outerWidth(width);
        }
    },
    time: {
        init: function (container, options) {
            var input = $('<input />').appendTo(container);
            setTimeout(function () {
                $(input).timespinner($.extend({}, options));
            });
            return input;
        },
        destroy: function (target) {
            $(target).remove();
        },
        getValue: function (target) {
            return $(target).timespinner('getValue')
        },
        setValue: function (target, value) {
            $(target).val(value);
        },
        resize: function (target, width) {
            $(target)._outerWidth(width);
        }
    }
});

/*-----------------------------------------------------------------------------
custom editors base (for extension)
-----------------------------------------------------------------------------*/
function custom_editor(base, name, options) {
    if (!options.panelHeight) {
        if (options.data && options.data.length > 15)
            options.panelHeight = 200;
    }
    $.fn.datagrid.defaults.editors[name] = $.extend({},
        $.fn.datagrid.defaults.editors[base],
        { options: options }
    );
}

function fmt_translate(vals, data, fromField, toField) {
    if (!vals || vals.length < 1) return vals;
    var vs = vals.split(',');
    var ns = [];
    $(data).each(function (k, v) {
        if ($.inArray(v[fromField], vs) >= 0)
            ns.push(v[toField]);
    });
    return ns.join(',');
}

function objs_contains(objs, obj) {
    if (objs == null) return false;
    for (var i = 0; i < objs.length; ++i) {
        if (JSON.stringify(objs[i]) == JSON.stringify(obj)) return true;
    }
    return false;
}

$.extend($.fn.datagrid.defaults.editors, {
    select: {
        defaults: {
            editable: false,
            panelHeight: 'auto',
            valueField: 'Name',
            textField: 'Name',
            labelField: 'Label',
            blankItem: false,
            loadFilter: function (objs) {
                var opts = $(this).combobox('options');
                if (opts.blankItem) {
                    var obj = {};
                    obj[opts.valueField] = null;
                    obj[opts.textField] = '&nbsp;';
                    if (!objs_contains(objs, obj))
                        objs.unshift(obj);
                }
                return objs;
            },
            formatter: function (row) {
                var opts = $(this).combobox('options');
                return (row[opts.labelField]) ? (row[opts.labelField] + ' (' + row[opts.textField] + ')') : (row[opts.textField]);
            }
        },
        init: function (container, options) {
            var opts = $.extend({}, this.defaults, options, this.options);
            var input = $('<input type="text" />').appendTo(container);
            setTimeout(function () {
                $(input).combobox(opts);
                if (val = $(input).attr('val')) {
                    $(input).combobox('setValue', val);
                    //$(input).combobox('setValues', val.split(','));
                }
            }, 0);
            return input;
        },
        destroy: function (target) {
            $(target).remove();
        },
        getValue: function (target) {
            //return $(target).combobox('getValues').join(',');
            return $(target).combobox('getValue');
        },
        setValue: function (target, value) {
            $(target).attr('val', value);
        },
        resize: function (target, width) {
            $(target)._outerWidth(width);
        }
    }
});

$.extend($.fn.datagrid.defaults.editors, {
    list: {
        defaults: {
            editable: false,
            multiple: true,
            idField: 'Name',
            textField: 'Name'
        },
        init: function (container, options) {
            options = $.extend({}, this.defaults, options, this.options, {
                onLoadSuccess: function (data) {
                    var grid = $(input).combogrid('grid');
                    var val = $(input).val();
                    $(val.split(',')).each(function (k, v) {
                        $(grid).datagrid('selectRecord', v);
                    });
                }
            });
            var input = $('<input type="text" />').appendTo(container);
            setTimeout(function () {
                $(input).combogrid(options);
            }, 0);
            return input;
        },
        destroy: function (target) {
            $(target).remove();
        },
        getValue: function (target) {
            return $(target).combogrid('getValues').join(',');
        },
        setValue: function (target, value) {
            $(target).val(value);
        },
        resize: function (target, width) {
            $(target)._outerWidth(width);
        }
    }
});

$.extend($.fn.datagrid.defaults.editors, {
    choice: {
        defaults: {
            editable: false,
            multiple: true,
            wholeItem: false,
            sortable: false,
            panelHeight: 'auto',
            valueField: 'Name',
            textField: 'Name',
            loadFilter: function (objs) {
                var opts = $(this).combobox('options');
                if (opts.wholeItem) {
                    var obj = {};
                    obj[opts.valueField] = '*';
                    obj[opts.textField] = '*';
                    if (!objs_contains(objs, obj))
                        objs.unshift(obj);
                }
                return objs;
            },
            onSelect: function (record) {
                var opts = $(this).combobox('options');
                if (opts.wholeItem) {
                    if (record[opts.valueField] == '*')
                        $(this).combobox('setValues', ['*']);
                    else
                        $(this).combobox('unselect', '*');
                }
            },
            formatter: function (row) {
                var opts = $(this).combobox('options');
                return (row[opts.labelField]) ? (row[opts.labelField] + ' (' + row[opts.textField] + ')') : (row[opts.textField]);
            }
        },
        init: function (container, options) {
            var opts = $.extend({}, this.defaults, options, this.options);
            var input = $('<input type="text" />').appendTo(container);
            setTimeout(function () {
                $(input).combobox(opts);
                if (val = $(input).attr('val'))
                    $(input).combobox('setValues', val.split(','));
            }, 0);
            return input;
        },
        destroy: function (target) {
            $(target).remove();
        },
        getValue: function (target) {
            var opts = $(target).combobox('options');
            var vals = $(target).combobox('getValues');
            if (opts.sortable) {
                var data = $(target).combobox('getData');
                var vs = [];
                $(data).each(function (k, v) {
                    var f = v[opts.valueField];
                    if (vals.indexOf(f) >= 0)
                        vs.push(f);
                });
                vals = vs;
            }
            return vals.join(',');
        },
        setValue: function (target, value) {
            $(target).attr('val', value);
        },
        resize: function (target, width) {
            $(target)._outerWidth(width);
        }
    }
});

/*-----------------------------------------------------------------------------
special editors 
<program>: need Application.js include. 
-----------------------------------------------------------------------------*/
$.extend($.fn.datagrid.defaults.editors, {
    program: {
        init: function (container, options) {
            options = $.extend(options, {
                //panelHeight: 350,
                url: new Application().ListProgram(),
                loadFilter: function (data) {
                    $(data).each(function (k, v) {
                        v.id = escape(v.Path);
                        v.text = v.Path;
                        v.state = v.IsProgram ? 'opened' : 'closed';
                        if (v.Path.length <= 3)
                            v.iconCls = 'icon-save';
                        if (v.IsProgram)
                            v.iconCls = 'icon-ok';
                    });
                    return data;
                },
                formatter: function (val) {
                    return val.Name;
                },
                onHidePanel: function () {
                    var node = $(this).combotree('tree').tree('getSelected');
                    var path = node ? unescape(node.id) : null;
                    var ext = path ? path.substring(path.length - 4).toLowerCase() : null;
                    if (ext != '.exe')
                        $(this).combotree('setValue', $(this).val())
                }
            });
            var input = $('<ul></ul>').appendTo(container);
            setTimeout(function () {
                var width = $(input).attr('w');
                if (width > 0)
                    options.width = width;
                $(input).combotree(options);
            }, 0);
            return input;
        },
        destroy: function (target) {
            $(target).remove();
        },
        getValue: function (target) {
            return $(target).combotree('getText');
        },
        setValue: function (target, value) {
            $(target).val(value);
        },
        resize: function (target, width) {
            $(target)._outerWidth(width);
            $(target).attr('w', width);
        }
    }
});
