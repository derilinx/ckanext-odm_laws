this.ckan.module('datepicker-module', function($, _) {
  return {
    initialize: function() {

      $('#field-odm_date_created').daterangepicker({
          singleDatePicker: true,
          showDropdowns: true
        });

      $('#field-odm_date_uploaded').daterangepicker({
          singleDatePicker: true,
          showDropdowns: true
        });

      $('#field-odm_date_modified').daterangepicker({
          singleDatePicker: true,
          showDropdowns: true
        });

      $('#field-odm_laws_version_date').daterangepicker({
          singleDatePicker: true,
          showDropdowns: true
        });

      $('#field-odm_laws_date_of_enactment').daterangepicker({
          singleDatePicker:true,
          showDropdowns:true
      });

      $('#field-odm_laws_final_action').daterangepicker({
        singleDatePicker:true,
        showDropdowns:true
      });

      $('#field-odm_laws_efective_date').daterangepicker({
        singleDatePicker:true,
        showDropdowns:true
      });
    }
  }
});

this.ckan.module('daterangepicker-module', function($, _) {
  return {
    initialize: function() {

      $('#field-odm_temporal_range').daterangepicker();

    }
  }
});
