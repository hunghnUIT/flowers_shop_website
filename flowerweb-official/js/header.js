
/* Search setting*/
$(window).on('scroll', function () {
    $('nav').toggleClass('black', window.scrollY >250);
    $('nav').toggleClass('sticky-top', window.scrollY <=250);
});
$('.modal-body-custom').click(function (e) { 
    if ($(e.target).is('#input-group *') || $(e.target).is('.modal-change-address *'))
    {
        return;
    }
    else
    {
        $('.modal').modal('hide');
    }
});
/**
 * Created by DELL on 5/2/2020.
 */
var isMobile = function() {
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        return true;
    }

    return false;
};
$(document).ready(function () {
    if (window.scrollY==0)
    {
        $('nav').addClass('sticky-top');
    }
    $('#search-box').focus();
    $('.login-span').click(function (e) { 
        window.location.replace("/login");
        console.log("login");
    });
    $('.register-span').click(function (e) { 
        window.location.replace("/register");
        console.log("register");
    });
});

