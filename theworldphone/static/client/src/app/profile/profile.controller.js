(function() {
  'use strict';

  angular
    .module('worldphone.profile')
    .controller('ProfileCtrl', ProfileCtrl);

  ProfileCtrl.$inject = ['$scope', '$state', 'auth', 'store', 'LanguageService', 'UserService', 'ratingIcons'];

  function ProfileCtrl($scope, $state, auth, store, LanguageService, UserService, ratingIcons) {
    var vm = this;

    vm.user = store.get('user');
    vm.user.spokenLanguages = vm.user.spokenLanguages || [];
    vm.user.learningLanguages = vm.user.learningLanguages || [];
    vm.languageOptions = LanguageService.all();

    vm.addLanguage = addLanguage;
    vm.addLanguageByName = addLanguageByName;
    vm.removeLanguage = removeLanguage;
    vm.availableLanguages = availableLanguages;

    vm.updateUser = updateUser;
    vm.onboardUser = onboardUser;
    vm.userData = userData;

    vm.ratingIcons = ratingIcons;

    new UserService.resource().$countries().then(function(response) {
      vm.countries = response;
      vm.countriesArray = [];
      angular.forEach(vm.countries, function(countryName, countryCode) {
        if (angular.isString(countryName))
          vm.countriesArray.push({ 'code': countryCode, 'name': countryName });
      });
    });

    function addLanguage(language, languages) {
      var languageIndex = vm.availableLanguages(languages).indexOf(language);
      if (languageIndex != -1 && LanguageService.has(language.attributes.name)) {
        languages.push(language);

        $scope.addingLanguage = false;
        $scope.showList = false;
        $scope.languageSearch = '';

        new UserService.resource(vm.userData()).$languages({id: vm.user.uid});
      }

      return languages;
    }

    function addLanguageByName(languageName, languages) {
        var language;
        angular.forEach(vm.languageOptions, function(languageOption) {
          if (languageOption.attributes.name.toLowerCase() == languageName.toLowerCase()) {
              language = languageOption;
              // angular.forEach is UNBREAKABLE
          }
        });
        return addLanguage(language, languages);
    }

    function removeLanguage(language, languages) {
      var languageIndex = languages.indexOf(language);
      if (languageIndex != -1 && LanguageService.has(language.attributes.name))
        languages.splice(languageIndex, 1);

        new UserService.resource(vm.userData()).$languages({id: vm.user.uid});

      return languages;
    }

    function availableLanguages(takenLanguages) {
      var takenLanguageNames = [];
      angular.forEach(takenLanguages, function(takenLanguage) {
        takenLanguageNames.push(takenLanguage.attributes.name);
      });
      return vm.languageOptions.filter(function(l) { return takenLanguageNames.indexOf(l.attributes.name) == -1; });
    }

    function updateUser(details) {
      if (details.nickname)
        vm.user.nickname = details.nickname;
      if (details.gender)
        vm.user.gender = details.gender;
      if (details.country)
        vm.user.location = details.country;

      new UserService.resource(userData()).$update({id: vm.user.uid}).then(function(response) {
          console.log('User updated');
          store.set('user', vm.user);
          if (vm.editing)
            vm.editing = false;
        }, function(error) {
          console.error('User not updated', error);
        });
    }

    function onboardUser(onboarding) {
      if (onboarding.$invalid) {
        console.log('Invalid form submission');
        return false;
      }

      vm.user.gender = onboarding.gender;
      vm.user.location = onboarding.country;
      vm.user.status = 'active';

      var spokenLanguage = angular.fromJson(onboarding.spokenLanguage);
      var learningLanguage = angular.fromJson(onboarding.learningLanguage);
      if (vm.user.spokenLanguages.indexOf(spokenLanguage) == -1)
        vm.user.spokenLanguages.push(spokenLanguage);
      if (vm.user.learningLanguages.indexOf(learningLanguage) == -1)
        vm.user.learningLanguages.push(learningLanguage);

      var userData = vm.userData();
      userData['data']['relationships']['ratings'] = {
        'overall': onboarding.ratings.overall.value,
        'vocabulary': onboarding.ratings.vocabulary.value,
        'grammar': onboarding.ratings.grammar.value,
        'accent': onboarding.ratings.accent.value
      };

      new UserService.resource(userData).$update({id: vm.user.uid}).then(function(response) {
          console.log('User updated');
          vm.user.ratings = response.data.attributes.ratings.data;
          store.set('user', vm.user);

          $state.go('profile');
        }, function(error) {
          console.error('User not updated', error);
        });
    }

    function userData() {
      var user = vm.user;
      var userData = {
        'id': user.uid,
        'data': {
          'type': 'user',
          'attributes': {
            'name': user.nickname,
            'email': user.email,
            'gender': user.gender,
            'location': user.location,
            'status': user.status,
          },
          'relationships': {
            'spoken_languages': {
              'data': user.spokenLanguages
            },
            'learning_languages': {
              'data': user.learningLanguages
            }
          }
        }
      };
      return userData;
    }
  }

})();
