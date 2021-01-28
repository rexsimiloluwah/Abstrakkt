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

let pdfDiv = document.getElementById('pdfDiv');
let rawDiv = document.getElementById('rawDiv');
let urlDiv = document.getElementById('urlDiv');
let originalTime = document.getElementById('original_time');
let summarizedTime = document.getElementById("summarized_time");
let summarizedText= document.getElementById("summarized-text");
const uploadedFile = document.getElementById("uploadedFile");
const form = document.getElementById("form");
const loader = document.querySelector(".loading");
const summarized = document.querySelector(".summarized");
const error = document.querySelector(".error")

let mode = null

$('#mode').change( function(){
    mode = $(this).val();
    if($(this).val() == "pdf"){
        pdfDiv.style.display = "block";
        rawDiv.style.display = "none";
        urlDiv.style.display = "none";
    }
    else{
        pdfDiv.style.display = "none";
    }
});
$("#mode").trigger("change");

$('#mode').change( function(){
    mode = $(this).val();
    if($(this).val() == "raw_text"){
        pdfDiv.style.dislay = "none";
        rawDiv.style.display = "block";
        urlDiv.style.display = "none";
       
    }
    else{
        rawDiv.style.display = "none";
    }
});
$("#mode").trigger("change");

$('#mode').change( function(){
    mode = $(this).val();
    if($(this).val() == "url"){
        pdfDiv.style.dislay = "none";
        rawDiv.style.display = "none";
        urlDiv.style.display = "block";
       
    }
    else{
        urlDiv.style.display = "none";
    }
});
$("#mode").trigger("change");

let fileLabel = document.getElementById("fileLabel");
let fileInput = document.getElementById("fileInput");
let fileLabelInner = fileLabel.innerHTML
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
    document.cookie = `filesize = ${element.files[0].size}`  
}

form.addEventListener("submit", (e) => {
    e.preventDefault();
    /* Initialize XMLHTTPRequest */
    let formData = new FormData();
    summarized.style.display = "none";
    loader.style.display = "block";
    $("#keywords").empty()
    $("#summarized-text").empty()
    $(".error").empty()
    let xhr = new XMLHttpRequest();
    switch(mode){
        case "raw_text":
        case "url":
            const data = {raw_text : e.target.rawText.value, url : e.target.url.value}
            xhr.open('POST', `/summarize?mode=${mode}`, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            console.log(data)
            xhr.onreadystatechange = function() { 
                console.log("Loading")
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                    console.log("Done")
                }
            }

            xhr.onload = function () {
                const response = JSON.parse(this.responseText);
                console.log(this.status)
                loader.style.display = "none"

                if(this.status === 200){
                    summarized.style.display = "block"
                    originalTime.innerText = `${response.original_reading_time} MINS`;
                    summarizedTime.innerText = `${response.reading_time} MINS`;
                    summarizedText.innerHTML = `<p>${response.summarized_text}</p>`;
                    
                    response.keywords.forEach(keyword => {
                        $("#keywords").append(`<p><span class = 'text--rebecca'>${keyword.word} :-</span> ${keyword.definition}</p>`)
                    })
                    console.log(response)
                }
                else{
                    error.style.display = "block"
                    error.innerHTML = `<p><i class="fa fa-exclamation-circle"></i> ${response.error}</p>`
                    console.log(response)
                }
            }
            /* POST THE DATA */
            xhr.send(JSON.stringify(data));
            break;
        case "pdf":
            let formData = new FormData();
            let file = fileInput.files[0];
            /* VALIDATION PROCESS - Check File Type and Size */
            if (!file.type.match('pdf.*')) {
                console.log("Only pdf files are allowed for now.")
            }

            // If file size is greater than 3MB, Do not process [Can be modified]
            if(file.size > 10 * 1024 * 1024){
                console.log("File size is too large to process.")
            }
            
            /* Add the file to the form for the AJAX request */
            formData.append('file', file);
            let f = {}
            for (let pair of formData.entries()){
                console.log(pair[0], pair[1])
            }
            xhr.open('POST', '/summarize/upload', true);
            xhr.onreadystatechange = function() { 
                console.log("Loading")
                loader.style.display = "none"
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                    console.log("Done")
                }
            }
            xhr.onload = function(){
                const response = JSON.parse(this.responseText);
                console.log(this.status)
                if(this.status === 200){
                    summarized.style.display = "block"
                    originalTime.innerText = `${response.original_reading_time} MINS`;
                    summarizedTime.innerText = `${response.reading_time} MINS`;
                    response.summarized_pages.forEach(page => {
                        $("#summarized-text").append(`<div><h6 class = "text--rebecca">PAGE :- ${page.page + 1}</h6> <p>${page.summarized_text}</p></div>`)
                    })
                    response.keywords.forEach(keyword => {
                        $("#keywords").append(`<p><span class = 'text--rebecca'>${keyword.word} :-</span> ${keyword.definition}</p>`)
                    })
                    console.log(response)
                }
                else{
                    error.style.display = "block"
                    error.innerHTML = `<p><i class="fa fa-exclamation-circle"></i> ${response.error}</p>`
                    console.log(response)
                }
            }

            /* POST THE DATA */
            xhr.send(formData);
        default: 
            break;
    }
})


  