odoo.define('techspawn_custom_module.custom_monetary', function (require) {
	"use strict";
var FieldChar = require('web.basic_fields').FieldChar;
var fieldRegistry = require('web.field_registry');
var CustomFieldChar = FieldChar.extend({
 description: _lt("CustomMonetary"),
    className: 'o_field_monetary o_field_number',
    tagName: 'span',
    supportedFieldTypes: ['float', 'monetary','integer'],
    resetOnAnyFieldChange: true, // Have to listen to currency changes

    /**
     * Float fields using a monetary widget have an additional currency_field
     * parameter which defines the name of the field from which the currency
     * should be read.
     *
     * They are also displayed differently than other inputs in
     * edit mode. They are a div containing a span with the currency symbol and
     * the actual input.
     *
     * If no currency field is given or the field does not exist, we fallback
     * to the default input behavior instead.
     *
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);

        this._setCurrency();

        if (this.mode === 'edit') {
            this.tagName = 'div';
            this.className += ' o_input';

            // do not display currency symbol in edit
            this.formatOptions.noSymbol = true;
        }

        this.formatOptions.currency = this.currency;
        this.formatOptions.digits = [16, 2];
        this.formatOptions.field_digits = this.nodeOptions.field_digits;
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * For monetary fields, 0 is a valid value.
     *
     * @override
     */
    isSet: function () {
        return this.value === 0 || this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * For monetary fields, the input is inside a div, alongside a span
     * containing the currency symbol.
     *
     * @override
     * @private
     */
    _renderEdit: function () {
        this.$el.empty();

        // Prepare and add the input
        var def = this._prepareInput(this.$input).appendTo(this.$el);

        if (this.currency) {
            // Prepare and add the currency symbol
            var $currencySymbol = $('<span>', {text: this.currency.symbol});
            if (this.currency.position === "after") {
                this.$el.append($currencySymbol);
            } else {
                this.$el.prepend($currencySymbol);
            }
        }
        return def;
    },
    /**
     * @override
     * @private
     */
    _renderReadonly: function () {
        this.$el.html(this._formatValue(this.value));
    },
    /**
     * Re-gets the currency as its value may have changed.
     * @see FieldMonetary.resetOnAnyFieldChange
     *
     * @override
     * @private
     */
    _reset: function () {
        this._super.apply(this, arguments);
        this._setCurrency();
    },
    /**
     * Deduces the currency description from the field options and view state.
     * The description is then available at this.currency.
     *
     * @private
     */
    _setCurrency: function () {
        var currencyField = this.nodeOptions.currency_field || this.field.currency_field || 'currency_id';
        var currencyID = this.record.data[currencyField] && this.record.data[currencyField].res_id;
        this.currency = session.get_currency(currencyID);
        this.formatOptions.currency = this.currency; // _formatValue() uses formatOptions
    },
});
fieldRegistry.add('custom_monetary', CustomFieldChar);

});
