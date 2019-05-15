(function() {
  'use strict';

  angular
    .module('worldphone.call')
    .factory('CallService', CallService)
    .factory('CallLogService', CallLogService);

    CallService.$inject = ['$resource'];
    CallLogService.$inject = ['$resource'];

  function CallService($resource) {
    return $resource('/api/v1/calls', {},
      {
        token: {
          method: 'GET',
          url: '/api/v1/calls/token/:userUid'
        },
        topics: {
          method: 'GET',
          url: '/api/v1/calls/topics/'
        },
        make: {
          method: 'POST',
          url: '/api/v1/calls/'
        },
        end: {
          method: 'PATCH',
          url: '/api/v1/calls/'
        },
      }
    );
  }

  function CallLogService($resource) {
    return $resource('/api/v1/call_logs/:id', {},
      {
        query: { // Get call history for user
          method: 'GET',
          url: '/api/v1/call_logs/:userUid'
        },
        update: {
          method: 'PATCH',
          url: '/api/v1/call_logs/:id'
        },
        rate: {
          method: 'PATCH',
          url: '/api/v1/call_survey/:sid'
        }
      }
    );
  }

})();
