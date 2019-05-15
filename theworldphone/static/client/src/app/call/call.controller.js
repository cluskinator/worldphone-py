(function() {
  'use strict';

  angular
    .module('worldphone.call')
    .controller('CallCtrl', CallCtrl);

  CallCtrl.$inject = ['$http', '$stateParams', '$state', '$scope', 'store',
                      'UserService', 'CallLogService', 'CallService', 'ratingIcons'];

  function CallCtrl($http, $stateParams, $state, $scope, store,
                    UserService, CallLogService, CallService, ratingIcons) {
    var vm = this;

    vm.ratingIcons = ratingIcons;

    // Menu
    vm.menu = {};
    vm.setMenuSections = setMenuSections;
    vm.activeSection = '';
    vm.isActive = isActive;
    vm.menuExpanded = false;
    vm.menuHovered = false;
    vm.menuOpened = menuOpened;
    vm.sectionActive = false;
    vm.toggleMenu = toggleMenu;
    vm.toggleMenuDetails = toggleMenuDetails;

    // Call
    // vm.callLogUid, vm.sid, vm.identity, vm.partner
    // vm.activeConversation, vm.conversationsClient, vm.previewMedia

    vm.endCall = endCall;
    vm.submitSurvey = submitSurvey;

    makeCall();

    // Remove users from queue if they leave
    window.onbeforeunload = function(e) {
      if (vm.waiting || vm.activeConversation)
        vm.endCall();
    }
    $scope.$on('$destroy', function(e) {
      if (vm.waiting || vm.activeConversation)
        vm.endCall();
      window.onbeforeunload = undefined;
    });

    // Make call
    function makeCall() {
      // Redirect to new call page if not in or waiting for call
      if (!$stateParams.callLanguages || !$stateParams.callType)
        return $state.go('newCall');

      var user = store.get('user');

      new CallService().$token({userUid: user.uid}).then(function(response) {
        var token = response.token;
        vm.identity = response.identity; // user's uid

        vm.conversationsClient = new Twilio.Conversations.Client(token);
        vm.conversationsClient.listen().then(clientConnected, function(error) {
          log('Could not connect to Twilio: ' + error.message);
        });
      });
    }

    // Call: Successfully connected!
    function clientConnected() {
      log('Connected to Twilio');

      new CallService(callQueueData()).$make().then(function(response) {
        var results = response.data.attributes;
        vm.waiting = results.waiting;

        if (vm.waiting) {
          log('Queued'); // "Queued as '" + vm.identity + "' in '" + results.queue_name + "'"

        } else {
          vm.partner = results.partner;
          vm.callLogUid = results.call_log_uid;
          log('Connecting to partner'); // "Connecting to partner '" + vm.partner + "' as '" + vm.identity + "'"

          if (vm.activeConversation) {
            // Add a participant
            vm.activeConversation.invite(vm.partner);

          } else {
            // Create a conversation
            var options = {};
            if (vm.previewMedia)
              options.localMedia = vm.previewMedia;

            vm.conversationsClient.inviteToConversation(vm.partner, options).then(conversationStartedWithLog, function (error) {
              console.error('Unable to create conversation', error);
              retryCall();
            });
          }
        }
      });

      vm.conversationsClient.on('invite', function (invite) {
        if (!vm.partner) {
          vm.partner = invite.from;
          log('Matched - connecting to partner'); // "Matched - connecting to '" + vm.partner + "'"
          invite.accept().then(conversationStarted);
        }
      });
    }

    // Call: Conversation is live
    function conversationStarted(conversation) {
      log('In an active conversation');
      vm.activeConversation = conversation;
      vm.sid = vm.activeConversation.sid;

      // When a participant joins, draw their video on screen
      vm.activeConversation.on('participantConnected', function (participant) {
        log('Participant connected'); // "Participant '" + participant.identity + "' connected"
        vm.setMenuSections();
        participant.media.attach('#remote-media');

        // Draw local video, if not already previewing
        if (!vm.previewMedia && !vm.activeConversation.localMedia.videoTracks.length) {
          vm.activeConversation.localMedia.attach('#local-media');
        }
      });

      // When a participant disconnects, perform post-call actions
      vm.activeConversation.on('participantDisconnected', function (participant) {
        log('Participant disconnected'); // "Participant '" + participant.identity + "' disconnected"
        vm.endCall();

        $scope.$evalAsync(function() {
          $scope.showSurvey = true;
        });
      });

      // When the conversation ends, stop capturing local video
      vm.activeConversation.on('ended', function (conversation) {
        log('Conversation ended');
        vm.activeConversation.localMedia.stop();
        vm.activeConversation.localMedia.videoTracks.detach();
        vm.activeConversation.disconnect();
      });
    }

    function conversationStartedWithLog(conversation) {
      conversationStarted(conversation);
      logCall();
    }

    // Retry call
    function retryCall() {
      log('Retrying call');

      if (vm.callLogUid) {
        log('Removing call log for failed connection');
        new CallLogService().$delete({id: vm.callLogUid}).then(function(response) {
          log('Call log for failed connection has been removed');
        });
      }

      resetCall();
      log('Retrying call');
      makeCall();
    }

    // End call
    function endCall() {
      log('Ending call');

      vm.conversationsClient.unlisten();

      var callData = callQueueData();
      if (vm.callLogUid)
        callData.data.attributes['call_log_uid'] = vm.callLogUid;

      new CallService(callData).$end().then(function(response) {
        log('Call end logged');
      }, function(error) {
        console.error('Error ending call', error);
      });

      if (vm.activeConversation) {
        log('Disconnecting active conversation');
        vm.activeConversation.disconnect();
      } else {
        log('Unqueueing');
        resetCall();
        $state.go('newCall');
      }
    }

    function resetCall() {
      vm.callLogUid = null;
      vm.partner = null;
      vm.waiting = true;
    }

    // Log details about the call and both participants
    function logCall() {
      var callData = {
        'id': vm.callLogUid,
        'data': {
          'type': 'call_log',
          'attributes': {
            'caller_uid': vm.identity,
            'callee_uid': vm.partner,
            'call_sid': vm.activeConversation.sid,
            'call_type': $stateParams.callType
          }
        }
      };

      new CallLogService(callData).$update({id: vm.callLogUid}).then(function(response) {
        log('Call log updated');
      });
    }

    function log(message) {
      console.log('<<<[ ' + message + ' ]>>>');
    }

    function submitSurvey(surveyResponses) {
      var callData = {
        'id': vm.callLogUid,
        'data': {
          'type': 'call_log',
          'attributes': {
            'quality': surveyResponses['quality'].value,
            'flag': surveyResponses['flag'] || '',
            'comment': surveyResponses['comment'] || '',
            'current_user': vm.identity
          }
        }
      };

      new CallLogService(callData).$rate({sid: vm.sid}).then(function(response) {
        log('Call rated');
      }, function(error) {
        console.error('Unable to rate call', error);
      });

      var userData = {
        'id': vm.partner,
        'data': {
          'type': 'user',
          'attributes': {},
          'relationships': {
            'ratings': {
              'overall': surveyResponses['overall'].value,
              'grammar': surveyResponses['grammar'].value,
              'vocabulary': surveyResponses['vocabulary'].value,
              'accent': surveyResponses['accent'].value
            }
          }
        }
      };

      new UserService.resource(userData).$rate({id: vm.partner}).then(function(response) {
        log('User rated');
      }, function(error) {
        console.error('Unable to rate user', error);
      });

      resetCall();
      $state.go('newCall');
    }

    // Menu

    function menuOpened() {
      return (vm.menuExpanded || vm.menuHovered);
    }

    function toggleMenu() {
      if (vm.menuExpanded) {
        // Close menu
        vm.activeSection = '';
        vm.menuExpanded = false;
        vm.menuHovered = false;
      } else {
        // Open menu
        vm.activeSection = '';
        vm.menuExpanded = true;
        vm.menuHovered = false;
      }
    }

    function toggleMenuDetails(section) {
      if (isActive(section) || vm.menu[section].length <= 1) {
        // Close menu details
        vm.menuExpanded = false;
        vm.sectionActive = false;
        vm.activeSection = '';
        vm.activeSectionDetails = [];
      } else {
        // Open menu details
        vm.menuExpanded = true;
        vm.sectionActive = true;
        vm.activeSection = section;
        vm.activeSectionDetails = vm.menu[section];
      }
    }

    function isActive(section) {
      return vm.activeSection == section;
    }

    function setMenuSections() {
      vm.menu = { 'personal': [], 'topics': [], 'trends': [], 'region': [] };
      new UserService.resource().$get({id: vm.partner}).then(function(response) {
        var partner = response.data.attributes;
        vm.menu.personal = [partner.nickname + ' | ' + partner.fluent];
        vm.menu.region = [partner.country];

        new CallService().$topics().then(function(response) {
          vm.menu.topics = grabBag(response.data.attributes.topics);
          vm.menu.trends = grabBag(response.data.attributes.trends);

          // OK GO
          vm.waiting = false;
        });
      });
    }

    // Return 8 random from given topics/trends
    function grabBag(list) {
      var grabBag = list.sort(function() { return 0.5 - Math.random(); });
      return grabBag.slice(0, 8);
    }

    function callQueueData() {
      var user = store.get('user');
      var callData = {
        'data': {
          'type': 'call',
          'attributes': {
            'call_type': $stateParams.callType,
            'call_languages': $stateParams.callLanguages,
            'caller_identity': user.uid
          }
        }
      };

      return callData;
    }
  }

})();
