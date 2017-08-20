/**
 * editgrid - jQuery EasyUI
 */
(function ($) {
    function buildGrid(target) {
        var opts = $.data(target, 'formgrid').options;
        $(target).datagrid($.extend({}, opts, {
            onAfterEdit: function (index, row) {
                var dg = $(this);
                var url = row.isNewRecord ? opts.insertUrl : opts.updateUrl;
                if (url) {
                    $.post(url, row, function (data, status, jqx) {
                        if (!data.Exception) {
                            opts.editIndex = undefined;
                            data.isNewRecord = null;
                            $(target).datagrid('updateRow', { index: index, row: data });
                            opts.onSave.call(target, index, row);
                        }
                        else {
                            dg.datagrid('beginEdit', opts.editIndex);
                            dg.datagrid('selectRow', opts.editIndex);
                            opts.onError.call(target, index, data);
                        }
                    }, 'json');
                } else {
                    opts.onSave.call(target, index, row);
                }
                if (opts.onAfterEdit) opts.onAfterEdit.call(target, index, row);
            },
            onCancelEdit: function (index, row) {
                opts.editIndex = undefined;
                if (row.isNewRecord) {
                    $(this).datagrid('deleteRow', index);
                }
                if (opts.onCancelEdit) opts.onCancelEdit.call(target, index, row);
            },
            onBeforeLoad: function (param) {
                if (opts.onBeforeLoad.call(target, param) == false) { return false }
                $(this).datagrid('rejectChanges');
            }
        }));

        function focusEditor(field) {
            var editor = $(target).datagrid('getEditor', { index: opts.editIndex, field: field });
            if (editor) {
                editor.target.focus();
            } else {
                var editors = $(target).datagrid('getEditors', opts.editIndex);
                if (editors.length) {
                    editors[0].target.focus();
                }
            }
        }
    }

    $.fn.formgrid = function (options, param) {
        if (typeof options == 'string') {
            var method = $.fn.formgrid.methods[options];
            if (method) {
                return method(this, param);
            } else {
                return this.datagrid(options, param);
            }
        }

        options = options || {};
        return this.each(function () {
            var state = $.data(this, 'formgrid');
            if (state) {
                $.extend(state.options, options);
            } else {
                $.data(this, 'formgrid', {
                    options: $.extend({}, $.fn.formgrid.defaults, $.fn.formgrid.parseOptions(this), options)
                });
            }
            buildGrid(this);
        });
    };

    $.fn.formgrid.parseOptions = function (target) {
        return $.extend({}, $.fn.datagrid.parseOptions(target), {
        });
    };

    $.fn.formgrid.methods = {
        options: function (jq) {
            var opts = $.data(jq[0], 'formgrid').options;
            return opts;
        },
        enableEditing: function (jq) {
            return jq.each(function () {
                var opts = $.data(this, 'formgrid').options;
                opts.editing = true;
            });
        },
        disableEditing: function (jq) {
            return jq.each(function () {
                var opts = $.data(this, 'formgrid').options;
                opts.editing = false;
            });
        },
        editRow: function (jq) {
            return jq.each(function () {
                var dg = $(this);
                var opts = $.data(this, 'formgrid').options;
                //var editIndex = opts.editIndex;
                if (opts.editIndex >= 0) {
                    return;
                }
                else {
                    var row = dg.datagrid('getSelected');
                    if (!row) {
                        $.messager.show({
                            title: opts.tipMsg.norecord.title,
                            msg: opts.tipMsg.norecord.msg
                        });
                        return;
                    }
                    var idx = dg.datagrid('getRowIndex', row);
                    dg.datagrid('beginEdit', idx);
                    dg.datagrid('selectRow', idx);
                    opts.editIndex = idx;
                }
            });
        },
        addRow: function (jq, index) {
            return jq.each(function () {
                var dg = $(this);
                var opts = $.data(this, 'formgrid').options;
                if (opts.editIndex >= 0) {
                    dg.datagrid('selectRow', opts.editIndex);
                    return;
                }
                var rows = dg.datagrid('getRows');

                function _add(index, row) {
                    if (index == undefined) {
                        dg.datagrid('appendRow', row);
                        opts.editIndex = rows.length - 1;
                    } else {
                        dg.datagrid('insertRow', { index: index, row: row });
                        opts.editIndex = index;
                    }
                }
                if (typeof index == 'object') {
                    _add(index.index, $.extend(index.row, { isNewRecord: true }))
                } else {
                    _add(index, { isNewRecord: true });
                }

                dg.datagrid('beginEdit', opts.editIndex);
                dg.datagrid('selectRow', opts.editIndex);

                opts.onAdd.call(this, opts.editIndex, rows[opts.editIndex]);
            });
        },
        saveRow: function (jq) {
            return jq.each(function () {
                var dg = $(this);
                var opts = $.data(this, 'formgrid').options;
                if (opts.onBeforeSave.call(this, opts.editIndex) == false) {
                    setTimeout(function () {
                        dg.datagrid('selectRow', opts.editIndex);
                    }, 0);
                    return;
                }
                $(this).datagrid('endEdit', opts.editIndex);
            });
        },
        cancelRow: function (jq) {
            return jq.each(function () {
                var index = $(this).formgrid('options').editIndex;
                $(this).datagrid('cancelEdit', index);
            });
        },
        destroyRow: function (jq) {
            return jq.each(function () {
                var dg = $(this);
                var opts = $.data(this, 'formgrid').options;
                var row = dg.datagrid('getSelected');
                if (!row) {
                    $.messager.show({
                        title: opts.tipMsg.norecord.title,
                        msg: opts.tipMsg.norecord.msg
                    });
                    return;
                }
                $.messager.confirm(opts.tipMsg.confirm.title, opts.tipMsg.confirm.msg, function (r) {
                    if (r) {
                        var index = dg.datagrid('getRowIndex', row);
                        if (row.isNewRecord) {
                            dg.datagrid('cancelEdit', index);
                        } else {
                            if (opts.onBeforeDestroy.call(this, index) == false) {
                                setTimeout(function () {
                                    dg.datagrid('selectRow', index);
                                }, 0);
                                return;
                            }
                            if (opts.destroyUrl) {
                                var idValue = row[opts.idField || 'id'];
                                $.post(opts.destroyUrl, { id: idValue }, function (data, status, jqx) {
                                    if (data == true) {
                                        dg.datagrid('cancelEdit', index);
                                        dg.datagrid('deleteRow', index);
                                        opts.onDestroy.call(dg[0], index, row);
                                    }
                                    else {
                                        opts.onError.call(dg[0], index, data);
                                    }
                                }, 'json');
                            } else {
                                dg.datagrid('cancelEdit', index);
                                dg.datagrid('deleteRow', index);
                                opts.onDestroy.call(dg[0], index, row);
                            }
                        }
                    }
                });
            });
        }
    };

    $.fn.formgrid.defaults = $.extend({}, $.fn.datagrid.defaults, {
        editing: true,
        editIndex: -1,
        tipMsg: {
            norecord: {
                title: 'Warning',
                msg: 'No record is selected.'
            },
            confirm: {
                title: 'Confirm',
                msg: 'Are you sure you want to delete?'
            }
        },

        url: null, // return the datagrid data
        insertUrl: null, // return the added row
        updateUrl: null, // return the updated row
        destroyUrl: null, // return {success:true}

        onAdd: function (index, row) { },
        onEdit: function (index, row) { },
        onBeforeSave: function (index) { },
        onSave: function (index, row) { },
        onError: function (index, data) { },
        onBeforeDestroy: function (index) { },
        onDestroy: function (index, row) { }
    });
})(jQuery);