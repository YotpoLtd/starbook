STAR_BOOK_API = "https://hive-back.yotpo.com/api";
SEND_COOKIES = true;
FACEBOOK_APP_ID = '765762016914736';

angular.module('myApp')
  .constant("ENV", {
    "GOOGLE_SIGN_IN_CLIENT_ID": "some-client-id.apps.googleusercontent.com",
    "STAR_BOOK_API": STAR_BOOK_API,
    "SEND_COOKIES": SEND_COOKIES
  });
