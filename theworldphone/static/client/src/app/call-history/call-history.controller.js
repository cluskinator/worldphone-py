(function() {
  'use strict';

  angular
    .module('worldphone.callHistory')
    .controller('CallHistoryCtrl', CallHistoryCtrl);

  CallHistoryCtrl.$inject = ['store', 'CallLogService', 'LanguageService'];

  function CallHistoryCtrl(store, CallLogService, LanguageService) {
    var vm = this;
    vm.user = store.get('user');
    vm.languages = LanguageService.all();

    new CallLogService().$query({userUid: vm.user.uid}).then(function(response) {
      vm.callList = [];
      angular.forEach(response.data, function(callLogData) {
        var callLog = callLogData.attributes;

        var details = {};
        // Language will be switched if incoming call with more than one language
        details['language1'] = callLog.language1.data.attributes.name;
        details['start_time'] = callLog.start_time;
        details['duration'] = callLog.duration;
        details['call_type'] = callLog.call_type;
        if (callLog.caller_uid == vm.user.uid) {
          // User was caller
          details['direction'] = 'outgoing';
          details['partner_username'] = callLog.callee_username;
          if (callLog.language2)
            details['language2'] = callLog.language2.data.attributes.name;
        } else {
          // User was callee
          details['direction'] = 'incoming';
          details['partner_username'] = callLog.caller_username;
          if (callLog.language2) {
            details['language1'] = callLog.language2.data.attributes.name;
            details['language2'] = callLog.language1.data.attributes.name;
          }
        }

        vm.callList.push(details);
      });
    });
  }

})();
