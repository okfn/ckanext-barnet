"use strict";

ckan.module('barnet_frequency_field_hider', function ($, _){
  return {
    initialize: function () {
      $.proxyAll(this, /_option/);
      //option 1
      var frequency_update_period = this.$('#field-frequency_update_period');
      //option 2
      var frequency_count = this.$('#field-frequency_count');
      var frequency_period = this.$('#field-frequency_period');

      this._option_check();

      frequency_update_period.on('change', this._option_one_change);
      frequency_count.on('change', this._option_two_change);
      frequency_period.on('change', this._option_two_change);
    },

    _option_check: function(){
      this._option_one_check();
      this._option_two_check();
    },

    _option_one_check: function(){
      //option 1
      var frequency_update_period = this.$('#field-frequency_update_period');
      //option 2
      var frequency_count = this.$('#field-frequency_count');
      var frequency_period = this.$('#field-frequency_period');
      
      if(frequency_update_period.val() == '') {
        frequency_count.removeAttr('disabled');
        frequency_period.removeAttr('disabled');
      } else {
        frequency_count.attr('disabled', 'disabled');
        frequency_count.val('');
        frequency_period.attr('disabled', 'disabled');
        frequency_period.val('');
      }
    },

    _option_two_check: function(){
      //option 1
      var frequency_update_period = this.$('#field-frequency_update_period');
      //option 2
      var frequency_count = this.$('#field-frequency_count');
      var frequency_period = this.$('#field-frequency_period');
      
      if(frequency_count.val() == '' && frequency_period.val() == '') {
        frequency_update_period.removeAttr('disabled');
      } else {
        frequency_update_period.attr('disabled', 'disabled');
      }
    },

    _option_one_change: function(event) {
      this._option_one_check();
    },

    _option_two_change: function(event) {
      this._option_two_check();
    }
  };
});
