!function(){"use strict";function t(t,e,n){function i(){n.isAuthenticated()&&t.url("/")}function r(){n.register(o.email,o.password,o.username)}var o=this;o.register=r,i()}angular.module("thinkster.authentication.controllers").controller("RegisterController",t),t.$inject=["$location","$scope","Authentication"]}();