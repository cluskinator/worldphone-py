(function() {

  angular
    .module('worldphone')
    .directive('rating', rating);

    function rating() {
      return {
        replace: false,
        restrict: 'E',
        scope: {
          category: '@',
          icon: '@',
          rating: '='
        },
        templateUrl: 'templates/layout/_rating.html'
      }
    }

})();
