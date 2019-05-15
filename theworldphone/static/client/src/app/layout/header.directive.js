(function() {

  angular
    .module('worldphone')
    .directive('twpHeader', twpHeader);

    function twpHeader() {
      return {
        replace: true,
        templateUrl: '/templates/layout/header.html'
      }
    }

})();
