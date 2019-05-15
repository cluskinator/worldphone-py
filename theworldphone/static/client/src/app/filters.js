(function() {
  'use strict';

  angular
    .module('worldphone')
    .filter('percentage', percentage)
    .filter('titleize', titleize);

  percentage.$inject = ['$filter'];

  function percentage($filter) {
    return percentageFilter;

    function percentageFilter(input, decimals) {
      return $filter('number')(input * 100, decimals) + '%';
    }
  }

  function titleize() {
    return titleizeFilter;

    function titleizeFilter(str) {
      if (str)
        return str.replace(/\w\S*/g, function(s) { return s.charAt(0).toUpperCase() + s.substr(1).toLowerCase(); });
    }
  }

})();
