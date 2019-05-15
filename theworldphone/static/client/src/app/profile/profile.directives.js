(function() {

  angular
    .module('worldphone.profile')
    .directive('languages', languages)
    .directive('ratings', ratings);

    function languages() {
      return {
        controller: 'ProfileCtrl',
        controllerAs: 'profile',
        replace: true,
        restrict: 'E',
        scope: {
          languages: '='
        },
        templateUrl: 'templates/profile/_languages.html'
      }
    }

    function ratings() {
      return {
        controller: 'ProfileCtrl',
        controllerAs: 'profile',
        replace: true,
        restrict: 'E',
        scope: {
          category: '@',
          score: '@'
        },
        templateUrl: 'templates/profile/_ratings.html'
      }
    }

})();
