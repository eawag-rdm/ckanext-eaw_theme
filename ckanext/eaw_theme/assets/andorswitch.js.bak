// HvW -2016-06-27
/* Used by scheming/form_snippets/eaw_schema_checkbox.html
         + snippets/eaw_pkg_search_form.html      
         +  snippets/eaw_pkg_search_form.html
   Requires bootstrap-switch.js
   Provides js - switch to beautify checkbox.
   For different use-cases, the bootstrapSwitch can be
   parameterized with different sets of options, whic are selected
   through the argument "type", which is passed attribute "data-module-type"
   in the markup.
 */

"use strict"

ckan.module('andorswitch', function ($, _) {
  return {
    initialize: function () {
      var options;
      var optionset = {
	andor: {
	  onText: "ANY",
	  onColor: "primary",
	  offText: "ALL",
	  offColor: "info",
	  size: "normal",
	  animate: false
	},
	  yesno: {
	  onText: "YES",
	  onColor: "primary",
	  offText: "NO",
	  offColor: "default",
	  size: "normal",
	  animate: false
	}
      };
      options = this.options && ("type" in this.options) ?
      optionset[this.options["type"]] :
      optionset["andor"];
      this.el.bootstrapSwitch(options);
    }
  };
});

