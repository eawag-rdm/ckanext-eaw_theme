// Module to be bound to the "Advanced Search Button".
// Makes the button visible, implements toggling of
// the next element that contains helptext and searchbox,
// which it also hides.

"use strict"

ckan.module('eaw_theme_hidewithjs', function($, _) {
    return {
	initialize: function () {
	    var target = this.options.target;
	    var hidden = this.sandbox.jQuery( target );
	    var query = this.options.query;
	    this.el.show();
	  if (typeof query !== "string") {
	      hidden.css('visibility', 'hidden');
	    } else { 
	      hidden.css('visibility', 'visible');
	    }
	  this.el.click(function () {
	    var viz;
	    viz = hidden.css('visibility') === 'hidden' ? 'visible' : 'hidden';
	    console.log(viz);
	    hidden.css('visibility', viz);
	    return(false);
	    });
	}
    };
});
	    
