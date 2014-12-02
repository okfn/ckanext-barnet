"use strict";

ckan.module('barnet_dates', function ($, _){
  return {
    initialize: function () {
      this.$('input#field-next_update').datepicker({"dateFormat": "yy/mm/dd"});
      this.$('input#field-review_date').datepicker({"dateFormat": "yy/mm/dd"});
      this.$('input#field-coverage_start_date').datepicker({"dateFormat": "yy/mm/dd"});
      this.$('input#field-coverage_end_date').datepicker({"dateFormat": "yy/mm/dd"});
    }
  };
});
