$(function() {
  
    
    $(window).on('load', function(event) {
        $('.preloader').delay(500).fadeOut(500);
    });
});

$(function() {
    "use strict";

    /*-----------------------------------
     * FIXED  MENU - HEADER
     *-----------------------------------*/
    function menuscroll() {
        var $navmenu = $('.nav-menu');
        var $navbar = $('.navbar');
        var $navbarcollapse = $('.navbar-collapse');
        if ($(window).scrollTop() > 50) {
            $navmenu.addClass('is-scrolling');
            $navbar.addClass('is-scrolling');
            $navbarcollapse.addClass('is-scrolling');
        } else {
            $navmenu.removeClass("is-scrolling");
            $navbar.removeClass('is-scrolling');
            $navbarcollapse.removeClass('is-scrolling');
        }
    }
    menuscroll();
    $(window).on('scroll', function() {
        menuscroll();
    });
    /*-----------------------------------
     * NAVBAR CLOSE ON CLICK
     *-----------------------------------*/

    $('.navbar-nav > li:not(.dropdown) > a').on('click', function() {
        $('.navbar-collapse').collapse('hide');
    });
    /* 
     * NAVBAR TOGGLE BG
     *-----------------*/
    var siteNav = $('#navbar');
    siteNav.on('show.bs.collapse', function(e) {
        $(this).parents('.nav-menu').addClass('menu-is-open');
    })
    siteNav.on('hide.bs.collapse', function(e) {
        $(this).parents('.nav-menu').removeClass('menu-is-open');
    })
});

$(document).ready(function () {

    $('.first-button').on('click', function () {
  
      $('.animated-icon1').toggleClass('open');
    });
    $('.second-button').on('click', function () {
  
      $('.animated-icon2').toggleClass('open');
    });
    $('.third-button').on('click', function () {
  
      $('.animated-icon3').toggleClass('open');
    });
  });

  
const Typing = function(txtElement, words, wait=3000){

    this.txtElement = txtElement;
    this.words = words;
    this.txt = '';
    this.wordIndex = 0;
    this.type();
    this.wait = parseInt(wait, 10);
    this.isDeleting = false;
}
Typing.prototype.type = function() {
    const current = this.wordIndex;
     
    const fullTxt = this.words[current]

    if(this.isDeleting){
        this.txt = fullTxt.substring(0, this.txt.length - 1);
    }
    else{
        this.txt = fullTxt.substring(0, this.txt.length + 1);
    }
    //Insert new span tag into the tagline element for the Cursor
    this.txtElement.innerHTML = `<span class="txt">${this.txt}</span>`;

    //Set typing speed for the Timeout below
    let typingSpeed = 250;

    if(this.isDeleting){
        typingSpeed = typingSpeed /2;
    }

    //When the one of the Texts in the words array has been completely typed
    if(!this.isDeleting && this.txt === fullTxt){
        typingSpeed = this.wait;
        this.isDeleting = true;
        
    }
    else if(this.isDeleting && this.txt === ''){
        this.isDeleting = false;

        this.wordIndex++;
        typingSpeed = 300;
    }
   
if((this.wordIndex==4) && (this.txt === '')){
    this.wordIndex = 0;
}
    setTimeout(() => this.type(), typingSpeed);
}

//DOM initializer when the Website Loads
document.addEventListener('DOMContentLoaded', init)

function init(){
    const txtElement = document.querySelector('#tagline');
    const words = JSON.parse(txtElement.getAttribute('data-words'));
    const wait = txtElement.getAttribute('data-wait');
    new Typing(txtElement, words, wait);
}

const features = document.querySelector('.features');

const tl = new TimelineMax();

tl.fromTo(
    features,
    5, 
    {height: "0%"},
    {height: "20%",
    ease: Power2.easeInOut }
);

// $(document).ready(function() {
//     // Check if element is scrolled into view
//     function isScrolledIntoView(elem) {
//       var docViewTop = $(window).scrollTop();
//       var docViewBottom = docViewTop + $(window).height();
  
//       var elemTop = $(elem).offset().top;
//       var elemBottom = elemTop + $(elem).height();
  
//       return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
//     }
//     // If element is scrolled into view, fade it in
//     $(window).scroll(function() {
//       $('.features-card.animated').each(function() {
//         if (isScrolledIntoView(this) === true) {
//           $(this).addClass('fadeInUp');
//         }
//       });
//     });
//   });

var fieldGroup = document.getElementById('fieldGroup')
var pdfDiv = document.getElementById('pdfDiv')
var rawDiv = document.getElementById('rawDiv')
$('#fieldGroup').change( function(){

    if($(this).val() == "pdf"){
        pdfDiv.style.display = "block";
        rawDiv.style.display = "none";
        urlDiv.style.display = "none";
    }
    else{
        pdfDiv.style.display = "none";
    }
});
$("#fieldGroup").trigger("change");

$('#fieldGroup').change( function(){

    
    if($(this).val() == "raw-text"){
        pdfDiv.style.dislay = "none";
        rawDiv.style.display = "block";
        urlDiv.style.display = "none";
       
    }
    else{
        rawDiv.style.display = "none";
    }
});
$("#fieldGroup").trigger("change");

$('#fieldGroup').change( function(){

    
    if($(this).val() == "url-link"){
        pdfDiv.style.dislay = "none";
        rawDiv.style.display = "none";
        urlDiv.style.display = "block";
       
    }
    else{
        urlDiv.style.display = "none";
    }
});
$("#fieldGroup").trigger("change");


// File Upload Section
console.log("Yes !");

var fileLabel = document.getElementById("fileLabel");
var fileInput = document.getElementById("file");
var fileLabelInner = fileLabel.innerHTML

console.log(fileLabelInner);

console.log("shit")
fileInput.addEventListener('change', function(e){
var fileName = " ";
fileName = e.target.value.split("fakepath").pop();
        
fileLabel.innerHTML = `<span style="font-size:10px;"> ${fileName} <span class='fa fa-check' style='color: springgreen;margin-left: 12px; margin-top: 10px;margin-bottom:auto;'></span></span>`;

        fileLabel.style.border = "1px solid rgb(52,13,224)"
        fileLabel.style.boxShadow = "2px 2px 1px -1px rgba(58, 19,158)"
})


function filesize(element){
    console.log(element.files[0].size)

    //Saving it as a cookie for accessibility in the Flask application
    document.cookie = `filesize = ${element.files[0].size}`  //Using the string interpolation syntax in Javascript 
    }


  