!function(n,t){"use strict";function r(){function r(r,e){e=t.extend({timeout:3e3},e),e.content=r,n.snackbar(e)}function e(n,t){r("Error: "+n,t)}function o(n,t){r(n,t)}var c={error:e,show:o};return c}angular.module("thinkster.utils.services").factory("Snackbar",r)}($,_);