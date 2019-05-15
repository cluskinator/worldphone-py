(function() {
  'use strict';

  angular
    .module('worldphone.newCall')
    .controller('NewCallCtrl', NewCallCtrl);

  NewCallCtrl.$inject = ['store', 'LanguageService'];

  function NewCallCtrl(store, LanguageService) {
    var vm = this;
    vm.languageOptions = LanguageService.all();
    vm.user = store.get('user');

    vm.callerIdentity = vm.user.nickname;
  }

})();
