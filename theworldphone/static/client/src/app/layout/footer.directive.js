(function() {

  angular
    .module('worldphone')
    .directive('twpFooter', twpFooter);

    function twpFooter() {
      return {
        replace: true,
        templateUrl: '/templates/layout/footer.html'
      }
    }

})();
