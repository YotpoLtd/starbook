angular.module('myApp')
  .constant("ENV", {
    "GOOGLE_SIGN_IN_CLIENT_ID": window.env_vars['GOOGLE_SIGN_IN_CLIENT_ID'],
    "HIVE_API": window.env_vars['HIVE_API'],
    "SEND_COOKIES": window.env_vars['SEND_COOKIES']
  });
