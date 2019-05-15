(function() {

  angular
    .module('worldphone')
    .directive('modal', modal);

    function modal() {
      return {
        replace: true,
        restrict: 'E',
        scope: {
          show: '=',
          closeable: '='
        },
        transclude: true,
        templateUrl: 'templates/layout/_modal.html',
        link: function($scope, element, attrs) {
          $scope.modalStyle = {};
          if (attrs.width)
            $scope.modalStyle.width = attrs.width;
          if (attrs.height)
            $scope.modalStyle.height = attrs.height;

          $scope.hideModal = function() {
            if ($scope.closeable)
              $scope.show = false;
          };
        }
      }
    }

})();
