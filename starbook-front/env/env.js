STAR_BOOK_API = "http://192.168.99.100:5000/api";
SEND_COOKIES = false;

angular.module('myApp')
  .constant("ENV", {
    "GOOGLE_SIGN_IN_CLIENT_ID": "some-client-id.apps.googleusercontent.com",
    "STAR_BOOK_API": STAR_BOOK_API,
    "SEND_COOKIES": SEND_COOKIES
  });
