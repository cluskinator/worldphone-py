(function() {
  'use strict';

  angular
    .module('worldphone')

    .constant('ratingIcons', {
      'overall': 'star',
      'grammar': 'book',
      'vocabulary': 'file-text',
      'accent': 'comment',
      'skill': 'user'
    });

})();
